import json
import os

file_map = {
    'java-rt-jar-stubs-1.5.0.jar' : 'src-jdk7',
    'hibernate-core-5.2.10.Final.jar': 'hibernate-core',
    'wicket-core-7.8.0.jar': 'wicket-core',
    'apache-commons' : 'apache-commons',
    'apache-xalan' : 'apache-xalan',
    'encoder-1.2.1.jar' : 'owasp-encoder',
    'apache-xmlrpc' : 'apache-xmlrpc',
    'apache-stratos' : 'apache-stratos',
    'pebble' : 'pebble',
    'spring-web-4.3.9.RELEASE.jar' : 'spring-web',
    'esapi-2.0_rc10.jar' : 'owasp-esapi',
    'spring-context' : 'spring-context',
    'google-oauth2' : 'google-oauth2',
    'apache-shiro' : 'apache-shiro',
    'spring-jdbc' : 'spring-jdbc',
    'jsoup' : 'jsoup',
    'spring-security' : 'spring-security',
    'spring-core' : 'spring-core',
    'xmldb' : 'xmldb',
    'spring-websocket' : 'spring-websocket',
    'spring-expression' : 'spring-expression',
    'owasp-html' : 'owasp-html',
    'owasp-json' : 'owasp-json',
    'apache-axis2' : 'apache-axis2',
    'apache-commons-io' : 'apache-commons-io',
    'scribejava' : 'scribejava',
    'apache-commons-jxpath' : 'apache-commons-jxpath',
    'apache-bcel' : 'apache-bcel',
    'dmfs' : 'dmfs',
    'novell' : 'novell',
    'tomcat-5.5-servlet-api.jar' : 'tomcat55',
    'apache-xerces' : 'apache-xerces'
}

root_dir = "data"

def main():
    with open('data.json', 'r') as file:
        data = file.read().replace('\n', ' ')
    loaded_methods = json.loads(data)["methods"]

    for method in loaded_methods:
        type = method["type"]
        dir = file_map[method["jar"]]
        name = os.sep.join(method["name"].split(".")[:-1]) + ".java"
        path = os.path.join(root_dir, dir, name)
        if not os.path.exists(path):
            print(path)

   # print(loaded_methods[0].keys())

if __name__ == "__main__":
    main()