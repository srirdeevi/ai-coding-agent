from planner import Planner


planner = Planner()


question = "Where is authentication implemented?"


plan = planner.create_plan(question)


print("Planner Decision:")
print("------------------")

print(plan)
