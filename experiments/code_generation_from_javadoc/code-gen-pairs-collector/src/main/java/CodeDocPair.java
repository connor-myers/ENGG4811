public class CodeDocPair {

    private String code;
    private String doc;

    public CodeDocPair(String code, String doc) {
        this.code = code;
        this.doc = doc;
    }

    public String getCode() {
        return code;
    }

    public String getDoc() {
        return doc;
    }

    @Override
    public String toString() {
        return String.format("Code=%s;Doc=%s", this.code, this.doc);
    }
}
