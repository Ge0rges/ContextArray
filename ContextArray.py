import math


class ContextArray:
    """
    An array that updates itself based on the current computing context in order to find elements that are more likely
    to appear soon, faster. This is based on the encoding specificity principle of the brain.
    Insert: O(1)
    updateContext: O(n * number of contextual elements)
    delete: O(find)
    find: O(n) but we suppose average to be better
    """

    # elements[i]'s context is at contexts[i]
    __elements = []
    __contexts = []

    def insert(self, element, context):
        """Inserts the element into the array and attaches it's insertion context to it.
        :param element: Any object that can be used as a key to a dict
        :type element: Object
        :param context: A list of context items. These can be any non None object.
        :type context: List

        """
        self.__elements.insert(0, element)
        self.__contexts.insert(0, context)

    def update_context(self, context):
        """
        Updates the ordering of the array based on the passed context. We assume that this will improve the average case
        of find() and delete() by moving things up to the front of the array when the context is familiar.

        This is an expensive function which is meant to call it's content on a seprate background thread (which it
        currently does not do).

        :param context:
        :type context: List
        """

        new_elements = self.__elements.copy()
        new_contexts = self.__contexts.copy()

        # For each element
        for i in range(len(self.__elements)):
            # Get it's context
            element_context = self.__contexts[i]

            # Calculate the score of the context (how familiar it is)
            similar_contextual_elements = 0
            for contextualElement in context:
                if contextualElement in element_context:
                    similar_contextual_elements += 1

            score = similar_contextual_elements/len(element_context)

            # Score the element with the current context
            new_index = len(self.__contexts) - 1 - math.floor(score * (len(self.__contexts)-1))

            # Based on score calculate the new index for this element
            new_elements.insert(new_index, new_elements.pop(i))
            new_contexts.insert(new_index, new_contexts.pop(i))

        self.__elements = new_elements
        self.__contexts = new_contexts

    def delete(self, element):
        """
        Deletes an object from the array.

        :param element: The object to be deleted.
        :type element: Object
        :return: None
        :rtype: None
        """
        index = self.find(element)
        self.__elements.pop(index)
        self.__contexts.pop(index)

    def find(self, element):
        """
        Returns the index where element is located, -1 if not located.

        :param element: The element we wish to find.
        :type element: Object
        :return: index where element is located, -1 if not located.
        :rtype: Integer
        """
        for i in range(len(self.__elements)):
            if element == self.__elements[i]:
                return i
        return -1
