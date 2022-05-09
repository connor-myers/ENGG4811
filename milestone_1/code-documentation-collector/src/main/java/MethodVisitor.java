import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.printer.configuration.PrettyPrinterConfiguration;

import java.util.List;
import java.util.Locale;

public class MethodVisitor extends VoidVisitorAdapter<List<CodeDocPair>> {
    @Override
    public void visit(MethodDeclaration md, List<CodeDocPair> pairs) {
        super.visit(md, pairs);
        if (md.getBody().isPresent() && md.getJavadocComment().isPresent()) {
            //String code = cleanCode((md.getBody().get().toString())); // no method signature inc
            String code = cleanCode(md.getDeclarationAsString() + " " + md.getBody().get()); // method signature inc
            String doc = cleanDocumentation(md.getJavadocComment().get().getContent());

            if (code.length() == 0 || doc.length() == 0) {
                return;
            }

            CodeDocPair pair = new CodeDocPair(code, doc);
            pairs.add(pair);
        }
    }

    private String cleanDocumentation(String raw) {
        return raw.
                replaceAll("\n", " "). // remove new lines
                replace("*", ""). // removes stars that create comments
                replaceAll("<[^>]*>", ""). // remove html
                replaceAll("http\\S+", ""). // remove links
                replaceAll("/\\s\\s+/g", " ").
                replaceAll("\t", " "). // replace tabs with spaces
                replaceAll(" +", " "). // multiple spaces replaced with a single space
                trim();
    }

    private String cleanCode(String raw) {
        return raw. // removes opening and closing braces
                replaceAll("\n", " "). // remove new lines
                replaceAll("//.*|/\\*(?s:.*?)\\*/|(\"(?:(?<!\\\\)(?:\\\\\\\\)*\\\\\"|[^\r\n\"])*\")", "$1"). // remove comments
                replaceAll("/\\s\\s+/g", " ").
                replaceAll("\t", " "). // replace tabs with spaces
                replaceAll(" +", " "). // multiple spaces replaced with a single space
                trim(); // remove leading white space
    }
}
