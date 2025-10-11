import matplotlib.pyplot as plot
import jinja2
import argparse

parser = argparse.ArgumentParser(description="Process -s or -c arguments.")
parser.add_argument('-s', type=str, help='Value for student id')
parser.add_argument('-c', type=str, help='Value for course id')
args = parser.parse_args()

error_t = """<!DOCTYPE html>
<html>
    <head>
        <title>Something went wrong</title>
    </head>
    <body>
        <h1>Wrong input</h1>
        <p>Something went wrong</p>
    </body>
</html>
"""

if args.c:
    # print(f"c: {args.c}")
    highest = -1
    tot_marks = 0
    count = 0
    marks_freq: dict[int, int] = {}
    course_found = False

    with open("data.csv") as f:
        f.readline()  # Skip header
        for line in f:
            line = line.strip().split(",")
            if int(args.c) == int(line[1]):
                course_found = True
                highest = max(highest, int(line[2]))
                tot_marks += int(line[2])
                count += 1
                if line[2] in marks_freq:
                    marks_freq[int(line[2])] += 1
                else:
                    marks_freq[int(line[2])] = 1

    if course_found:
        plot.bar(list(marks_freq.keys()), list(marks_freq.values()))
        plot.xlabel("Marks")
        plot.ylabel("Frequency")
        plot.title("Marks Frequency Distribution for Course id: " + args.c)
        plot.savefig(f"./{args.c}.png")
        plot.close()

        # print(f"Highest marks: {highest}")
        # print(f"Average marks: {tot_marks / count if count > 0 else 0}")

        t = jinja2.Template(open("./course_temp.html").read())
        details = t.render(avg_marks=tot_marks / count if count > 0 else 0, max_marks=highest, course_id=args.c)
    else:
        details = error_t

    with open("output.html", "w") as f:
        f.write(details)

    # print(details)

elif args.s:
    # print(f"s: {args.s}")

    details = []
    stud_found = False
    tot_marks = 0
    with open("data.csv") as f:
        f.readline()  # Skip header
        for line in f:
            line = line.strip().split(",")
            if int(args.s) == int(line[0]):
                stud_found = True
                line[0] = line[0].strip()  # Clean spaces from student id
                line[1] = line[1].strip()  # Clean spaces from name
                line[2] = line[2].strip()  # Clean spaces from course id
                details.append(line)
                tot_marks += int(line[2])  # Assuming marks are in the third column

    if stud_found:
        t = jinja2.Template(open("./stud_temp.html").read())
        details = t.render(details=details, total_marks=tot_marks)
    else:
        details = error_t

    with open("output.html", "w") as f:
        f.write(details)

    # print(details)
else:
    # print("No arguments provided.")
    with open("output.html", "w") as f:
        f.write(error_t)