import yaml
from file import FileProcessor

def main():
    bruh = FileProcessor("test.yaml").load()
    for package in bruh:
        package.print()

    # with open('test.yaml', 'r') as file:
    #     packages = yaml.safe_load(file)
    #
    # # print(prime_service['prime_numbers'][0])
    # # print(prime_service['rest']['url'])
    # print(packages['packages'][0]["package"]["sources"])

if __name__ == "__main__":
    main()