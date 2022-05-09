import org.json.simple.JSONObject;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Main {

    public static int TOTAL_CHANCE = 100;
    public static int POSITIVE_CHANCE = 50;

    public static int NEGATIVE_CHANCE = TOTAL_CHANCE - POSITIVE_CHANCE;
    public static int NUM_EXAMPLES = 6000;

    public static double NUM_TRAIN = 0.8;
    public static double NUM_TEST = 0.1;
    public static double NUM_EVAL = 0.1;

    public static int MAX_TOKEN_LENGTH = 510;
    public static void main(String[] args) {
        List<CodeDocPair> trainingPairs = LoadExamples.getExampleCodeDocPairs("examples_train");
        Collections.shuffle(trainingPairs);

        List<CodeDocPair> testingPairs = LoadExamples.getExampleCodeDocPairs("examples_test");
        Collections.shuffle(testingPairs);

        List<CodeDocPair> evaluatingPairs = LoadExamples.getExampleCodeDocPairs("examples_eval");
        Collections.shuffle(evaluatingPairs);


        List<JSONObject> trainExamples = generateExamples(trainingPairs, (int) Math.round(NUM_TRAIN * NUM_EXAMPLES));
        List<JSONObject> testExamples =   generateExamples(testingPairs, (int) Math.round(NUM_TEST * NUM_EXAMPLES));
        List<JSONObject> evalExamples =   generateExamples(evaluatingPairs, (int) Math.round(NUM_EVAL * NUM_EXAMPLES));

        // training data
        FileWriter train = null;
        FileWriter test = null;
        FileWriter valid = null;
        try {
            train = new FileWriter("data/train.jsonl");
            test = new FileWriter("data/test.jsonl");
            valid = new FileWriter("data/eval.jsonl");
        } catch (IOException e) {
            e.printStackTrace();
        }

        StringBuilder trainOutput = new StringBuilder();
        StringBuilder testOutput = new StringBuilder();
        StringBuilder evalOutput  = new StringBuilder();

        for (JSONObject trainExample : trainExamples) {
            trainOutput.append(trainExample.toJSONString()).append("\n");
        }
        trainOutput.setLength(trainOutput.length() - 1);
        for (JSONObject testExample : testExamples) {
            testOutput.append(testExample.toJSONString()).append("\n");
        }
        testOutput.setLength(testOutput.length() - 1);
        for (JSONObject evalExample : evalExamples) {
            evalOutput.append(evalExample.toJSONString()).append("\n");
        }
        evalOutput.setLength(evalOutput.length() - 1);

        System.out.printf("Num Training Examples = %d\n", trainExamples.size());

        try {
            train.write(trainOutput.toString());
            test.write(testOutput.toString());
            valid.write(evalOutput.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            train.close();
            test.close();
            valid.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<JSONObject> generateExamples(List<CodeDocPair> pairs, int num) {
        List<JSONObject> examples = new ArrayList<>();

        Random rand = new Random(System.currentTimeMillis());
        int numAdded = 0;
        int index = 0;
        while(numAdded < Integer.min(pairs.size(), num) && index < pairs.size()) {
            CodeDocPair pair = pairs.get(index);
            JSONObject example = new JSONObject();
            if (rand.nextInt(TOTAL_CHANCE) < POSITIVE_CHANCE) {
                // add a positive example
                example.put("code", pair.getCode());
                example.put("text", pair.getDoc());
                example.put("label", 1);
            } else {
                // add a negative example
                CodeDocPair otherPair;
                // need to make sure this pair we got isn't the same we will be combining it with
                do {
                    otherPair = pairs.get(rand.nextInt(pairs.size()));
                } while(otherPair == pair);

                example.put("code", pair.getCode());
                example.put("text", otherPair.getDoc());
                example.put("label", 0);
            }

            if (example.get("code").toString().length() + example.get("text").toString().length() < MAX_TOKEN_LENGTH) {
                examples.add(example);
                numAdded++;
            }

            index++;
        }

        return examples;
    }
}
