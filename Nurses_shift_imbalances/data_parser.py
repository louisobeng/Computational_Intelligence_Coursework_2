from collections import defaultdict

def parse_dat_file(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    try:
        # Extract number of jobs
        job_line = next(line for line in lines if "Jobs" in line)
        num_jobs = int(job_line.split('=')[1].strip())
        jobs_start_index = lines.index(job_line) + 1
        job_info = []
        for line in lines[jobs_start_index:jobs_start_index + num_jobs]:
            parts = list(map(int, line.split()))
            job_info.append(tuple(parts))

        # Extract number of nurses
        qual_line = next(line for line in lines if "Qualifications" in line)
        num_nurses = int(qual_line.split('=')[1].strip())
        quals_start_index = lines.index(qual_line) + 1

        nurse_qualifications = defaultdict(list)
        for nurse_id, line in enumerate(lines[quals_start_index:quals_start_index + num_nurses]):
            tokens = line.replace(":", "").split()
            nurse_qualifications[nurse_id] = list(map(int, tokens))

    except Exception as e:
        raise ValueError(f"Error parsing file {filepath}: {e}")

    return num_jobs, num_nurses, job_info, nurse_qualifications