---
name: Definition of Done
about: Checklist to verify whether a feature or release is ready
title: "[DoD]: "
labels: ["DoD"]
assignees: []
---

## Purpose
This issue checks whether the application or a feature is **done** and **ready for release**.

---

## Functional Requirements
- [ ] Courses can be created  
- [ ] Students can be imported  
- [ ] CS50 and Moodle data can be uploaded  
- [ ] Grading is calculated correctly  
- [ ] Grades can be exported to Moodle  
- [ ] A grading overview is available  

---

## Correctness of Grading
- [ ] Passed and failed assignments match CS50 data  
- [ ] Percentages are calculated correctly  
- [ ] No missing grades exist  

---

## Error Handling and Validation
- [ ] Invalid files / file formats are rejected  
- [ ] Missing data does not crash the system  
- [ ] Clear error messages are shown to the user  

---

## Security
- [ ] Only authorized users can export grades  

---

## Performance
- [ ] Imports and grading complete in reasonable time  
- [ ] User interface remains responsive  

---

## Usability
- [ ] Main workflows are intuitive  
- [ ] Error and success messages are clear  
- [ ] No manual database interaction is required  

---

## Testing
- [ ] Core functions (grading, import, export) are tested  
- [ ] All tests pass before release  
- [ ] No known critical bugs are open  

---

## Documentation
- [ ] arc42 documentation exists and is understandable  
- [ ] User workflows are documented  
- [ ] Guiding coding guidelines exist and are up to date  
- [ ] Known limitations are listed  

---

## Deployment and Build
- [ ] Application builds without errors  
- [ ] Configuration is environment-independent  
- [ ] Deployment steps are documented  

---

## Stakeholder Acceptance
- [ ] Tutor use cases are validated  
- [ ] Feedback is addressed or documented  
- [ ] Final approval is given  
