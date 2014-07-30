## Installation
I write dionysus's dependency graph on the basis of [pygraph](https://code.google.com/p/python-graph/). You can install it with easy_install. However, there is a bug in pydot, one of its dependencies. I recommend you install this [bug-free version](https://github.com/davidvilla/pydot) manually (typically python setup.py install). 

## My Components
You can find my code under core/dionysus/ directory. I have not document them well yet. Their functions are:

- dionysus_dependency_graph.py: class definition for dependency graph and many helper methods
- dionysus_algorithms.py: a costumed critical path algorithm for CPL calculation
- dionysus_schedule.py: scheduling algorithm implementation, e.g. Algorithm 2, 3 and 4 in dionysus paper
- test_ddg.py: a raw test case for classes and functions above
- Also you will see FR_case_step_x.png files. They are generate by scheduling code after every graph update.

## A Word about Failure Recovery Case
In dionysus paper, the scheduling order for FR case is (s5_1, s7, s2) -> (s8) -> (s3, s5_2, s6) -> (s4) -> (s1) in Figure 12(a); my simulating result is [s5_1, s7, s2] -> [s8, s4] -> [s3, s5_2, s6] -> [s1]. The reason that s4 is scheduled early is that I failed to let rule on s2 take enough long time to finish. In fact, s4 is waiting for resource from either s2 or s3. In simulation, update on s2 finished instantly, which give s4 the resource to go. 

## The End
I hope my work will help you and I can try to plug them in a NOX controller when I got time.
