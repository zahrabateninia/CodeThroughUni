# Write a class to receive 10 students name with their scores and then print the student's name with max score 
# and also the name of lowest score 

class ManageScores:
    def __init__(self):
        self.students = []  # List to hold (name, score) tuples

    def add_student(self, name, score):
        self.students.append((name, score))

    def get_highest_score_student(self):
        return max(self.students, key=lambda x: x[1])

    def get_lowest_score_student(self):
        return min(self.students, key=lambda x: x[1])


# Create an instance of ManageScores
score_manager = ManageScores()

numOfStudents = 10

for _ in range(numOfStudents):
    while True:
        entry = input("Enter the name and score for the student (e.g. Alice 15):\n")
        try:
            name, score = entry.split()
            score = float(score)
            if 0 <= score <= 20:
                score_manager.add_student(name, score)
                break
            else:
                print("Score must be between 0 and 20.")
                # Now ask only for the score again
                while True:
                    try:
                        score = float(input(f"Enter a valid score for {name} (0-20): "))
                        if 0 <= score <= 20:
                            score_manager.add_student(name, score)
                            break
                        else:
                            print("Score must be between 0 and 20.")
                    except ValueError:
                        print("Invalid score. Please enter a number.")
                break
        except ValueError:
            print("Invalid input format. Please enter name followed by score, e.g. 'Alice 15'.")



# Get highest and lowest score students
highest = score_manager.get_highest_score_student()
lowest = score_manager.get_lowest_score_student()

print(f"\nHighest score: {highest[0]} with {highest[1]}")
print(f"Lowest score: {lowest[0]} with {lowest[1]}")
