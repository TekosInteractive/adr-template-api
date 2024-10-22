import xml.etree.ElementTree as ET
import sys

xml_file_path = sys.argv[1]
output_file_path = sys.argv[2]

tree = ET.parse(xml_file_path)
root = tree.getroot()

with open(output_file_path, 'w') as output_file:
  for testsuite in root.iter('testsuite'):
    name = testsuite.get('name')
    tests = int(testsuite.get('tests'))
    assertions = int(testsuite.get('assertions'))
    errors = int(testsuite.get('errors'))
    warnings = int(testsuite.get('warnings'))
    failures = int(testsuite.get('failures'))
    skipped = int(testsuite.get('skipped'))
    time = float(testsuite.get('time'))

    output_file.write(f'\nTest Suite Name: {name}\n')
    output_file.write(f'Total Tests: {tests}\n')
    output_file.write(f'Total Assertions: {assertions}\n')
    output_file.write(f'Errors: {errors}\n')
    output_file.write(f'Warnings: {warnings}\n')
    output_file.write(f'Failures: {failures}\n')
    output_file.write(f'Skipped: {skipped}\n')
    output_file.write('-' * 20)

testsuite = next(root.iter('testsuite'), None)

if testsuite:
    name = testsuite.get('name')
    tests = int(testsuite.get('tests'))
    assertions = int(testsuite.get('assertions'))
    errors = int(testsuite.get('errors'))
    warnings = int(testsuite.get('warnings'))
    failures = int(testsuite.get('failures'))
    skipped = int(testsuite.get('skipped'))
    time = float(testsuite.get('time'))

    print(f'- Total Tests: {tests} \\')
    print(f'Total Assertions: {assertions} \\')
    print(f'Errors: {errors} \\')
    print(f'Warnings: {warnings} \\')
    print(f'Failures: {failures} \\')
    print(f'Skipped: {skipped}')