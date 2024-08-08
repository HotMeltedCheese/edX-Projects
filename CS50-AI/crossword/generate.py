import sys
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # iterate through all variables and check to see if word length is greater or less than var length

        #raise Exception("TEST")
        for slot in self.domains:
            itemsToRemove = set()

            # check to see length of word in domain matches var length
            for x in self.domains[slot]:
                if len(x) != slot.length:
                    itemsToRemove.add(x)
            self.domains[slot] = self.domains[slot] - itemsToRemove


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # store times for deletion
        itemsToKeep = set()

        # iterate through all items in domain and gather the point
        for xdomain in self.domains[x]:
            overlapLocation = self.crossword.overlaps[x,y]
            if overlapLocation == None:
                 continue

            # iterate through all y domains; check for intersection match
            for ydomain in self.domains[y]:
                if xdomain[overlapLocation[0]] == ydomain[overlapLocation[1]]:
                    itemsToKeep.add(xdomain)

        if len(itemsToKeep) == len(self.domains[x]):
            return False

        # filter out all items that block AC
        self.domains[x] = itemsToKeep
        return True


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # iterate through all domains creating arcs between
        if arcs == None:
            arcs = []
            for arcStart in self.domains:
                for arcEnd in self.crossword.neighbors(arcStart):
                    arcs.append((arcStart, arcEnd))

        while len(arcs) != 0:
            # gather starting and ending points of arc
            startingVar, endingVar = arcs.pop(0)
            # only add more arcs if changes made
            if self.revise(startingVar, endingVar):
                # return if no solution available
                if len(self.domains[startingVar]) == 0:
                    return False

                # add all arcs that need to be reevaulated due to change
                for neighboringVar in self.crossword.neighbors(startingVar)- {endingVar}:
                    arcs.append((neighboringVar, startingVar))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            try:
                assignment[var]
            except KeyError:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check for unary and arc inconsistency
        for arcStart in assignment:
            # unary check
            if arcStart.length != len(assignment[arcStart]):
                return False

            # arc check for words within assigment
            for arcEnd in assignment:
                if arcStart == arcEnd:
                    continue
                oll = self.crossword.overlaps[arcStart, arcEnd]
                if oll != None and assignment[arcStart][oll[0]] != assignment[arcEnd][oll[1]]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domainV = {x:0 for x in self.domains[var]}
        # filter out neighbors that are already assigned
        neighbors = self.crossword.neighbors(var)
        setToRemove = set()
        for x in neighbors:
            if x in assignment:
                setToRemove.add(x)
        neighbors -= setToRemove

        # iterate through all vars in domain
        for currentWord in domainV:
            for otherVar in neighbors:
                oll = self.crossword.overlaps[var, otherVar]

                # check for arc inconsistency and keep track of #
                for otherWord in self.domains[otherVar]:
                    if currentWord[oll[0]] != otherWord[oll[1]]:
                        domainV[currentWord] += 1

        return sorted([x for x in domainV], key=lambda x:domainV[x])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # init starting vals
        incomplete = list(set(self.domains.keys()) - set(assignment.keys()))
        incomplete.sort(key=lambda x: len(self.domains[x]))

        # check for tie in MRV if there is then check degrees
        if len(incomplete) > 1 and len(self.domains[incomplete[0]]) == len(self.domains[incomplete[1]]):
            peak, newOrder = len(self.domains[incomplete[0]]), []
            # gather all degrees where MRV is tied
            for x in incomplete:
                val = len(self.domains[incomplete[0]])
                if val == peak:
                    newOrder.append(x)
            # find highest degree
            newOrder.sort(key=lambda x: len(self.crossword.neighbors(x)))
            incomplete = newOrder

        return incomplete[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # return if assignment is solution
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)

        # iterate though all choices of current var domain
        for domainValue in self.order_domain_values(var, assignment):
            assignment[var] = domainValue

            # check if assignment violates AC then recurse until sol found
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if self.assignment_complete(assignment) and self.consistent(assignment):
                    return result
            del assignment[var]

        return None

    def backtrackKnowledge(assignment):
        #if self.assignment_complete(assignment) and self.consistent(assignment):
        #    return
        domainSave = deepcopy(self.domains)

        for x in self.domains:
            if x in assignment:
                self.domains[x] = assignment[x]
        self.ac3()
        return domainSave


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
