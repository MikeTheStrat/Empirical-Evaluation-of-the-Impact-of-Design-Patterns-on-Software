import os
import csv
from radon.complexity import cc_visit
from radon.metrics import h_visit
from radon.raw import analyze
from math import log

def calculate_maintainability_index(cc_total, h_total, loc_total):
    """Calculate maintainability index based on total cyclomatic complexity, Halstead volume, and total lines of code."""
    maintainability_index = 171 - 5.2 * log(h_total) - 0.23 * cc_total - 16.2 * log(loc_total)
    return max(0, min(maintainability_index, 100))  # Maintainability index is between 0 and 100

def calculate_metrics_for_project(directory):
    """Calculate maintainability metrics for all Python files in a project directory."""
    cc_total = 0
    h_total = 0
    loc_total = 0
    file_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as file_obj:
                        code = file_obj.read()
                        cc_analysis = cc_visit(code)
                        h_analysis = h_visit(code)
                        raw_analysis = analyze(code)
                        cc_total += sum(func.complexity for func in cc_analysis)
                        h_total += h_analysis.total.volume
                        loc_total += raw_analysis.loc
                        file_count += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    if file_count > 0:
        maintainability_index = calculate_maintainability_index(cc_total, h_total, loc_total)
        return maintainability_index
    else:
        return None

def write_metrics_to_csv(directory, csv_file):
    """Write maintainability metrics for all Python projects in a directory to a CSV file."""
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Project', 'Maintainability Index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in os.scandir(directory):
            if entry.is_dir():
                project_dir = entry.path
                maintainability_index = calculate_metrics_for_project(project_dir)
                if maintainability_index is not None:
                    writer.writerow({'Project': os.path.basename(project_dir), 'Maintainability Index': maintainability_index})

def main():
    directory = os.getcwd()  # Current working directory
    csv_file = 'maintainability_metrics.csv'
    write_metrics_to_csv(directory, csv_file)
    print(f"Maintainability metrics written to {csv_file}")

if __name__ == '__main__':
    main()