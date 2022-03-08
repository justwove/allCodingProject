from tldextract import extract as ex
import argparse

if __name__ == '__main__':
    
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('--projet', required=True)
    args = parser.parse_args()

    with open(f'clean_{args.projet}_burp_domains.txt', 'w') as f:
        with open(f'{args.projet}_burp_domains.txt') as d:
            domains = [i for i in d.readlines()]
            clean_domain = [i.replace('\n', '') for i in domains]
            root_domain = [ex(i) for i in clean_domain]
            root_domain = [f"{res[1]}.{res[2]}" if res[0] == '' else f"{res[0]}.{res[1]}.{res[2]}" for res in root_domain]
            root_domain = list(dict.fromkeys(root_domain))
            write = [f.write(i + '\n') for i in root_domain]

