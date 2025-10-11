import os
from flask import Flask, render_template, request, redirect, url_for
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "data.csv")
IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

app = Flask(__name__, template_folder="templates", static_folder="static")


def read_data():
	"""Read data.csv and return list of rows as tuples (student_id, course_id, marks)."""
	rows = []
	if not os.path.exists(DATA_FILE):
		return rows
	with open(DATA_FILE, newline="") as f:
		reader = csv.reader(f)
		headers = next(reader, None)
		for r in reader:
			if not r:
				continue
			# strip spaces
			r = [c.strip() for c in r]
			try:
				sid = int(r[0])
				cid = int(r[1])
				marks = int(r[2])
			except Exception:
				# skip malformed lines
				continue
			rows.append((sid, cid, marks))
	return rows


@app.route("/", methods=["GET", "POST"])
def index():
	# Single form submits 'mode' ('student' or 'course') and 'identifier'
	if request.method == "POST":
		mode = request.form.get("mode")
		identifier = request.form.get("identifier", "").strip()
		if not identifier:
			return render_template("index.html", error="Please enter an id")
		# Redirect to the correct view with query parameter name matching existing handlers
		if mode == "student":
			return redirect(url_for('student') + f"?s={identifier}")
		else:
			return redirect(url_for('course') + f"?c={identifier}")

	return render_template("index.html")


@app.route("/student", methods=["GET", "POST"])
def student():
	sid = request.values.get("s")
	if not sid:
		return render_template("student.html", error="No student id provided", details=None)
	try:
		sid_i = int(sid)
	except ValueError:
		return render_template("student.html", error="Invalid student id", details=None)

	rows = read_data()
	details = [("Course id", "Marks")]
	total = 0
	found = False
	student_rows = []
	for r in rows:
		if r[0] == sid_i:
			found = True
			student_rows.append({"course": r[1], "marks": r[2]})
			total += r[2]

	if not found:
		return render_template("student.html", error=f"Student id {sid_i} not found", details=None)

	return render_template("student.html", error=None, details=student_rows, total=total, student_id=sid_i)


@app.route("/course", methods=["GET", "POST"])
def course():
	cid = request.values.get("c")
	if not cid:
		return render_template("course.html", error="No course id provided", avg=None, maxm=None, img_path=None)
	try:
		cid_i = int(cid)
	except ValueError:
		return render_template("course.html", error="Invalid course id", avg=None, maxm=None, img_path=None)

	rows = read_data()
	marks = []
	for r in rows:
		if r[1] == cid_i:
			marks.append(r[2])

	if not marks:
		return render_template("course.html", error=f"Course id {cid_i} not found", avg=None, maxm=None, img_path=None)

	avg = sum(marks) / len(marks)
	maxm = max(marks)

	# frequency
	freq = {}
	for m in marks:
		freq[m] = freq.get(m, 0) + 1

	# create bar chart
	img_name = f"course_{cid_i}.png"
	img_path = os.path.join(IMAGES_DIR, img_name)
	plt.figure(figsize=(8, 4))
	plt.bar(list(freq.keys()), list(freq.values()), color="#4b7bec")
	plt.xlabel("Marks")
	plt.ylabel("Frequency")
	plt.title(f"Marks Frequency Distribution for Course id: {cid_i}")
	plt.tight_layout()
	plt.savefig(img_path)
	plt.close()

	# Use static path for template
	static_img_path = url_for('static', filename=f"images/{img_name}")

	return render_template("course.html", error=None, avg=avg, maxm=maxm, img_path=static_img_path, course_id=cid_i)


if __name__ == "__main__":
	# Run development server
	app.run(debug=True)

