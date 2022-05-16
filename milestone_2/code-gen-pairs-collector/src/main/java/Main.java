import org.json.simple.JSONObject;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Main {

    public static int NUM_EXAMPLES = 1000000;
    public static double NUM_TRAIN = 0.8;
    public static double NUM_TEST = 0.1;
    public static double NUM_EVAL = 0.1;

    public static int MAX_TOKEN_LENGTH = 350;
    public static void main(String[] args) {
        List<CodeDocPair> trainingPairs = LoadExamples.getExampleCodeDocPairs("../../milestone_1/code-documentation-collector/examples_train");
        Collections.shuffle(trainingPairs);

        System.out.println("Training pairs loaded" + trainingPairs.size() + " loaded");

        List<CodeDocPair> testingPairs = LoadExamples.getExampleCodeDocPairs("../../milestone_1/code-documentation-collector/examples_test");
        Collections.shuffle(testingPairs);

        System.out.println("Testing pairs loaded" + testingPairs.size() + " loaded");

        List<CodeDocPair> evaluatingPairs = LoadExamples.getExampleCodeDocPairs("../../milestone_1/code-documentation-collector/examples_eval");
        Collections.shuffle(evaluatingPairs);

        System.out.println("Evaluating pairs loaded: " + evaluatingPairs.size() + " loaded");

        System.out.println("Done getting pairs!");

        List<JSONObject> trainExamples = generateExamples(trainingPairs, (int) Math.round(NUM_TRAIN * NUM_EXAMPLES), false);
        List<JSONObject> testExamples =   generateExamples(testingPairs, (int) Math.round(NUM_TEST * NUM_EXAMPLES), true);
        List<JSONObject> evalExamples =   generateExamples(evaluatingPairs, (int) Math.round(NUM_EVAL * NUM_EXAMPLES), false);

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

    private static List<JSONObject> generateExamples(List<CodeDocPair> pairs, int num, boolean test) {
        List<JSONObject> examples = new ArrayList<>();

        int numAdded = 0;
        int index = 0;
        while(numAdded < Integer.min(pairs.size(), num) && index < pairs.size()) {
            System.out.printf("%d of %d\n", numAdded, Integer.min(pairs.size(), num));
            CodeDocPair pair = pairs.get(index);
            JSONObject example = new JSONObject();

            if (test) {
                example.put("code", "");
            } else {
                example.put("code", pair.getCode());
            }
            example.put("nl", pair.getDoc());

            if (example.get("code").toString().length() + example.get("nl").toString().length() < MAX_TOKEN_LENGTH) {
                examples.add(example);
                numAdded++;
            }

            index++;
        }

        return examples;
    }
}
