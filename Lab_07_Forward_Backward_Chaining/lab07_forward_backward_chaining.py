def forward_chaining(facts, rules):
    facts = set(facts)
    changed = True

    while changed:
        changed = False

        for conditions, conclusion in rules:
            if set(conditions).issubset(facts):
                if conclusion not in facts:
                    facts.add(conclusion)
                    changed = True

    return facts


def backward_chaining(goal, facts, rules, visiting=None):
    if goal in facts:
        return True

    if visiting is None:
        visiting = set()

    if goal in visiting:
        return False

    visiting = visiting | {goal}

    for conditions, conclusion in rules:
        if conclusion == goal:
            if all(
                backward_chaining(condition, facts, rules, visiting)
                for condition in conditions
            ):
                return True

    return False


rules = [
    (["fever", "cough"], "flu"),
    (["flu", "body_pain"], "infection"),
    (["infection"], "needs_rest"),
    (["fever", "headache"], "possible_illness"),
    (["possible_illness", "cough"], "medical_checkup")
]

initial_facts = {"fever", "cough", "body_pain"}

print("Initial Facts:", initial_facts)

derived_facts = forward_chaining(initial_facts, rules)

print("\nForward Chaining Results:")
for fact in sorted(derived_facts):
    print(fact)

goal = "needs_rest"

print("\nBackward Chaining")
print("Goal:", goal)

result = backward_chaining(goal, initial_facts, rules)

if result:
    print("Goal can be proved.")
else:
    print("Goal cannot be proved.")
