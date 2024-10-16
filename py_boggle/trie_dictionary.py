from typing import Dict, Optional, Iterator, Set

class TrieNode:
    """
    TrieNode class that holds the structure of each node in the Trie.
    """
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_word = False  # Marks if this node ends a word.


class TrieDictionary:
    """
    Trie-based implementation of BoggleDictionary.
    """

    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        """
        Load words from a file into the Trie.
        """
        try:
            # Read file, print OSError if cannot read
            with open(filename, 'r') as wordsfile:
                for line in wordsfile:
                    word = line.strip().lower()
                    current_node = self.root
                    for letter in word:
                        if letter not in current_node.children:
                            current_node.children[letter] = TrieNode()
                        current_node = current_node.children[letter]
                    current_node.is_word = True  # Mark the end of the word
        except OSError as e:
            raise OSError(f"Error opening or reading the file: {filename}") from e

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse the Trie to find the node that corresponds to the given prefix.
        If the prefix is found, return the corresponding TrieNode.
        If not, return None.
        """
        current_node = self.root
        for letter in prefix.lower():  # Handle case insensitivity
            if letter not in current_node.children:
                return None
            current_node = current_node.children[letter]
        return current_node

    def is_prefix(self, prefix: str) -> bool:
        """
        Check if the given prefix is valid in the Trie.
        """
        return self.traverse(prefix) is not None

    def contains(self, word: str) -> bool:
        """
        Check if the given word is in the Trie.
        """
        node = self.traverse(word)
        return node is not None and node.is_word

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over all the words in the Trie in lexicographic order.
        """
        def dfs(node: TrieNode, prefix: str):
            if node.is_word:
                yield prefix
            for letter, child_node in sorted(node.children.items()):
                yield from dfs(child_node, prefix + letter)

        # Start the DFS from the root of the Trie
        yield from dfs(self.root, '')

    def get_all_words(self) -> Set[str]:
        """
        Return a set containing all words stored in the Trie.
        This method uses the __iter__ method to collect all the words.
        """
        return set(self.__iter__())
