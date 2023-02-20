Alex says...

* Processes shouldn't be controlling each other. They shouldn't be relying on the inputs and outputs of one another.
  * Instead, there should be one shared memory where all the processes read and write from
  * If there are errors in one process, they will be propagated
  * If there is a manager service that delegates tasks to each process, that could work better?

Interactive test: testing that requires a human to validate whether it is working or not

* Write some unit tests (non-interactive testing)


## On Unit Testing
* For larger functions that have much input from upstream functions, test the upstream functions to ensure they're outputting the correct data.
* Break down larger functions into testable! bite sized pieces. Alex says they shouldn't be larger than the screen and they shouldn't need comments!


Use this for mocking API's: https://requests-mock.readthedocs.io/en/latest/index.html (if needed)