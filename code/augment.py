# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

# Synonym replacement from a dict added by Yury Kashnitskiy

from eda import *

# arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
ap.add_argument("--path_to_synonyms", required=False, type=str,
                help="path to a file with synonyms (tsv format)")
ap.add_argument("--lang", required=False, type=str, default='english',
                help="language (currently used only to load stopwords)")
ap.add_argument("--output", required=False, type=str, help="output file with augmented data")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha", required=False, type=float, help="percent of words in each sentence to be changed")
args = ap.parse_args()

# the output file
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join
    output = join(dirname(args.input), 'eda_' + basename(args.input))

# number of augmented sentences to generate per original sentence
num_aug = 9  # default
if args.num_aug:
    num_aug = args.num_aug

# how much to change each sentence
alpha = 0.1  # default
if args.alpha:
    alpha = args.alpha


# generate more data with standard augmentation
def gen_eda(train_orig, output_file, alpha, path_to_synonyms, num_aug=9):

    writer = open(output_file, 'w')
    lines = open(train_orig, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')
        label = parts[0]
        sentence = parts[1]
        aug_sentences = eda(sentence, alpha_sr=alpha, alpha_ri=alpha, alpha_rs=alpha,
                            p_rd=alpha, num_aug=num_aug, path_to_synonyms=path_to_synonyms)
        for aug_sentence in aug_sentences:
            writer.write(label + "\t" + aug_sentence + '\n')

    writer.close()
    print(f"generated augmented sentences with eda for {train_orig} to {output_file} with num_aug={num_aug}")


# main function
if __name__ == "__main__":

    # generate augmented sentences and output into a new file
    gen_eda(args.input, output, alpha=alpha, num_aug=num_aug, path_to_synonyms=args.path_to_synonyms)