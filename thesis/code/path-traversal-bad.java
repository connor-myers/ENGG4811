// https://samate.nist.gov/SARD/test-cases/2161/versions/1.0.0
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    String name = req.getParameter("name");
    conn = dataSrc.getConnection();
    conn.prepareStatement("SELECT * FROM users WHERE firstname LIKE '" + name + "'").executeQuery();
}