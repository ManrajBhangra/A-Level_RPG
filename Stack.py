class stack:
    # Creates class for stack

    def __init__(self):
        self.Enemies = []
        self.pointer = -1

    def push(self, item):
        ##### push #######
        # Parameters :- self, item
        # Return Type :- none
        # Purpose :- Adds an item to the stack
        ###########################
        self.Enemies.append(item)
        self.pointer += 1

    def pop(self):
        ##### pop #######
        # Parameters :- self
        # Return Type :- Last item added to the stack
        # Purpose :- Removes an item from the stack
        ###########################

        if self.Enemies is not []:
            self.pointer -= 1
            return self.Enemies.pop()

    def peek(self):
        ##### peek #######
        # Parameters :- self
        # Return Type :- Last item added to the stack
        # Purpose :- Gives the last item added to the stack without removing them
        ###########################
        if self.Enemies is not []:
            return self.Enemies[self.pointer]

    def erase(self):
        ##### erase #######
        # Parameters :- self
        # Return Type :- none
        # Purpose :- remove all items from a stack
        ###########################
        while self.pointer != -1:

            self.pop()

        self.pointer = -1
