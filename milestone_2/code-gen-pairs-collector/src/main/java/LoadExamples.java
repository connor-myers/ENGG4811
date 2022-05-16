import com.github.javaparser.ParseProblemException;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.visitor.VoidVisitor;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.TrueFileFilter;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class LoadExamples {
    public static List<CodeDocPair> getExampleCodeDocPairs(String projectsDirectory) {
        List<CodeDocPair> codeDocPairs = new ArrayList<>();

        File projects = new File(projectsDirectory);

        for (File project : projects.listFiles()) {
            if (!project.isDirectory()) {
                continue;
            }

            addExamplesFromProject(codeDocPairs, project);
        }

        return codeDocPairs;
    }

    private static void addExamplesFromProject(List<CodeDocPair> codeDocPairs, File project) {
        List<String> javaFilePaths = getJavaFileFilePaths(project);

        for (String javaFilePath : javaFilePaths) {
            FileInputStream fis = null;
            try {
                fis = new FileInputStream(javaFilePath);
            } catch (IOException e) {
                e.printStackTrace();
                continue;
            }

            CompilationUnit cu;
            try {
                cu = StaticJavaParser.parse(fis);
            } catch (ParseProblemException | StackOverflowError e) {
                // code contains invalid Java for some reason? Just ignore it.
                continue;
            }

            VoidVisitor<List<CodeDocPair>> methodNameVisitor = new MethodVisitor();
            methodNameVisitor.visit(cu, codeDocPairs);
        }
    }

    private static List<String> getJavaFileFilePaths(File project) {
        List<String> javaFilePaths = new ArrayList<>();

        List<File> files = (List<File>) FileUtils.listFiles(project, TrueFileFilter.INSTANCE, TrueFileFilter.INSTANCE);

        for (File file : files) {
            if (file.getName().endsWith(".java")) {
                javaFilePaths.add(file.getAbsolutePath());
            }
        }

        return javaFilePaths;
    }
}
