import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    if len(corpus[page]) == 0:
        totalProbabilities = {x : 1/len(corpus) for x in corpus}
        return totalProbabilities

    randomPageChance = (1 - damping_factor) / len(corpus)
    totalProbabilities = {x : randomPageChance for x in corpus}
    for x in totalProbabilities:
        if x in corpus[page]:
           totalProbabilities[x] += damping_factor / len(corpus[page])
    return totalProbabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    allPages = {x: 0 for x in corpus}
    page = random.choice(list(allPages))

    for currentIteration in range(0, n - 1):
        sample = transition_model(corpus, page, damping_factor)

        # use transition model data to generate the next page
        currentValue, targetValue = 0, random.random()
        for x in sample:
            currentValue += sample[x]
            if currentValue >= targetValue:
                page = x
                break
        allPages[page] += 1

    for x in allPages:
        allPages[x] /= n
    return allPages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # init staring Values
    values = [1/len(corpus), (1 - damping_factor)/len(corpus)]
    pageRanks, newPageRanks = {x: 1/len(corpus) for x in corpus}, {x: 1/len(corpus) for x in corpus}
    convergence = 1/len(corpus)
    highestConvergence = convergence

    # calculate page rank values while the amount change is above threshold
    while highestConvergence >= 0.001:
        for page in corpus:
            totalProbability = values[1]

            # check for all pages that lead to current page
            for iterPage in corpus:
                # if doesn't like to current page account for random page selection else else calculate using formula
                if len(corpus[iterPage]) == 0:
                    totalProbability += values[0]
                else:
                    totalProbability += damping_factor * pageRanks[iterPage]/len(corpus[iterPage])
        newPageRanks[page] = totalProbability

        total = sum(newPageRanks.values())
        for x in newPageRanks:
            newPageRanks[x] = newPageRanks[x] / total

        # find the greatest change made during calculations
        for x in corpus:
            convergence = abs(newPageRanks[x] - pageRanks[x])
            if highestConvergence < convergence:
                highestConvergence = convergence
        # copy list  for comparison
        pageRanks = newPageRanks.copy()

    return pageRanks

if __name__ == "__main__":
    main()
