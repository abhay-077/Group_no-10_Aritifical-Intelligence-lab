# LAB 07: Forward Chaining and Backward Chaining
# Aim: To implement Forward Chaining and Backward Chaining algorithms in
# Artificial Intelligence for logical reasoning and inference using facts and rules.


class Rule:
    """
    Represents an IF-THEN production rule:
    IF premise[0] AND premise[1] ... THEN conclusion
    """
    def __init__(self, premises, conclusion, rule_id=None):
        self.premises = list(premises)
        self.conclusion = conclusion
        self.rule_id = rule_id or f"IF ({' AND '.join(premises)}) THEN {conclusion}"

    def __repr__(self):
        return self.rule_id


# =====================================================================
# PART A: FORWARD CHAINING (DATA-DRIVEN REASONING)
# =====================================================================

def forward_chaining(rules, initial_facts, target_goal=None):
    """
    Forward Chaining (Bottom-Up, Data-Driven):
    Starts with known initial facts and applies inference rules (Modus Ponens)
    repeatedly to derive new facts until:
      1. Target goal is deduced, OR
      2. No new facts can be inferred (fixed point reached).
    """
    known_facts = set(initial_facts)
    inferred_order = []
    iteration = 1

    print(f"\n[Forward Chaining] Initial Known Facts: {sorted(list(known_facts))}")
    if target_goal:
        print(f"[Forward Chaining] Target Goal: '{target_goal}'")

    while True:
        new_fact_added = False
        print(f"\n  --- Iteration {iteration} ---")

        for rule in rules:
            # Check if all premises are satisfied and conclusion is not already known
            if all(p in known_facts for p in rule.premises) and rule.conclusion not in known_facts:
                print(f"    [FIRE] Rule '{rule.rule_id}' is satisfied.")
                print(f"           All premises {rule.premises} are true. Inferring '{rule.conclusion}'.")
                known_facts.add(rule.conclusion)
                inferred_order.append((rule, rule.conclusion))
                new_fact_added = True

                # Early exit if target goal reached
                if target_goal and rule.conclusion == target_goal:
                    print(f"    [SUCCESS] Target goal '{target_goal}' reached!")
                    return known_facts, inferred_order, True

        iteration += 1
        if not new_fact_added:
            print("    [STOP] No more rules can be fired (no new facts generated).")
            break

    goal_reached = (target_goal in known_facts) if target_goal else True
    return known_facts, inferred_order, goal_reached


# =====================================================================
# PART B: BACKWARD CHAINING (GOAL-DRIVEN REASONING)
# =====================================================================

def backward_chaining(goal, rules, known_facts, call_stack=None, depth=0):
    """
    Backward Chaining (Top-Down, Goal-Driven):
    Starts from the target goal and recursively verifies whether rules and
    known facts can prove the goal.
    Features:
      - Cycle detection using call_stack to avoid infinite recursion.
      - Graceful handling of unknown facts.
      - Clear indented trace of the proof tree.
    """
    if call_stack is None:
        call_stack = []

    indent = "    " * depth

    print(f"{indent}-> Checking Goal: '{goal}'")

    # Base Case 1: Goal is already a known fact
    if goal in known_facts:
        print(f"{indent}   [FACT FOUND] '{goal}' is directly given in known facts.")
        return True, [f"Fact: '{goal}' is known"]

    # Base Case 2: Cycle detection (Goal is currently being evaluated in call stack)
    if goal in call_stack:
        print(f"{indent}   [CYCLE DETECTED] Goal '{goal}' is in active stack {call_stack}. Aborting branch to prevent loop.")
        return False, [f"Cycle detected for '{goal}'"]

    # Find candidate rules that conclude the current goal
    candidate_rules = [r for r in rules if r.conclusion == goal]
    if not candidate_rules:
        print(f"{indent}   [FAILED] No rule concludes '{goal}' and it is not a known fact.")
        return False, [f"No rule concludes '{goal}'"]

    # Add goal to active call stack for cycle protection
    call_stack.append(goal)

    # Try each candidate rule
    for rule in candidate_rules:
        print(f"{indent}   Trying Rule: {rule.rule_id}")
        all_premises_proven = True
        sub_proofs = []

        for premise in rule.premises:
            success, proof_steps = backward_chaining(premise, rules, known_facts, call_stack, depth + 1)
            sub_proofs.extend(proof_steps)
            if not success:
                all_premises_proven = False
                print(f"{indent}   Premise '{premise}' could NOT be proven. Backtracking...")
                break

        if all_premises_proven:
            # Rule proved successfully
            call_stack.pop()
            print(f"{indent}   [PROVEN] Rule '{rule.rule_id}' satisfied. Concluded '{goal}'.")
            return True, sub_proofs + [f"Derived '{goal}' using {rule.rule_id}"]

    call_stack.pop()
    return False, [f"Failed to prove '{goal}'"]


# =====================================================================
# MAIN DRIVER FUNCTION
# =====================================================================

def main():
    print("=" * 70)
    print(" LAB 07: FORWARD CHAINING AND BACKWARD CHAINING")
    print("=" * 70)

    # -------------------------------------------------------------
    # PART A: Forward Chaining Demonstration
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART A: FORWARD CHAINING (DATA-DRIVEN INFERENCE)")
    print(" Rules:")
    print("   Rule 1: If A and B are true -> Infer C")
    print("   Rule 2: If C is true        -> Infer D")
    print(" Initial Facts: A, B")
    print("=" * 70)

    rules_a = [
        Rule(premises=['A', 'B'], conclusion='C', rule_id="Rule 1 (A, B -> C)"),
        Rule(premises=['C'], conclusion='D', rule_id="Rule 2 (C -> D)")
    ]
    initial_facts_a = {'A', 'B'}

    all_facts, inferences, reached = forward_chaining(rules_a, initial_facts_a, target_goal='D')

    print("\n[FORWARD CHAINING RESULTS]:")
    print(f"  Initial Facts:        {sorted(list(initial_facts_a))}")
    print(f"  All Inferred Facts:   {[c for _, c in inferences]}")
    print(f"  Complete Knowledge:   {sorted(list(all_facts))}")
    print(f"  Target 'D' Inferred?  {reached}")

    # Forward chaining extended: Deriving E
    print("\n[FORWARD CHAINING EXTENDED: DERIVING GOAL 'E']")
    rules_a_extended = rules_a + [Rule(premises=['D'], conclusion='E', rule_id="Rule 3 (D -> E)")]
    all_facts_e, inferences_e, reached_e = forward_chaining(rules_a_extended, initial_facts_a, target_goal='E')
    print(f"  Target 'E' Inferred via Forward Chaining? {reached_e} (Derived Facts: {[c for _, c in inferences_e]})")

    # -------------------------------------------------------------
    # PART B: Backward Chaining Demonstration
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART B: BACKWARD CHAINING (GOAL-DRIVEN RECURSION)")
    print(" Rules:")
    print("   Rule 1: A and B imply C")
    print("   Rule 2: C implies D")
    print("   Rule 3: D implies E")
    print(" Initial Facts: A, B")
    print(" Goal: E")
    print("=" * 70)

    rules_b = [
        Rule(premises=['A', 'B'], conclusion='C', rule_id="Rule 1 (A & B -> C)"),
        Rule(premises=['C'], conclusion='D', rule_id="Rule 2 (C -> D)"),
        Rule(premises=['D'], conclusion='E', rule_id="Rule 3 (D -> E)")
    ]
    initial_facts_b = {'A', 'B'}
    target_goal_b = 'E'

    print(f"\n[BACKWARD CHAINING TRACE FOR GOAL '{target_goal_b}']:")
    is_proven, proof_steps = backward_chaining(target_goal_b, rules_b, initial_facts_b)

    print(f"\n[BACKWARD CHAINING RESULT]:")
    print(f"  Can goal '{target_goal_b}' be proven? -> {is_proven}")
    print("  Proof Chain:")
    for step_num, step in enumerate(proof_steps, 1):
        print(f"    {step_num}. {step}")

    # -------------------------------------------------------------
    # EDGE CASE TESTS: Unknown Fact and Cyclic Rules
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" EDGE CASE 1: UNKNOWN FACT HANDLING")
    print(" Goal: 'Z' (No rule or fact leads to Z)")
    print("=" * 70)
    unknown_proven, _ = backward_chaining('Z', rules_b, initial_facts_b)
    print(f"Result: Can 'Z' be proven? -> {unknown_proven} (Handled gracefully)")

    print("\n" + "=" * 70)
    print(" EDGE CASE 2: CYCLIC RULES CYCLE DETECTION")
    print(" Rules have a circular loop: P -> Q, and Q -> P.")
    print(" Facts: empty. Goal: P.")
    print("=" * 70)
    cyclic_rules = [
        Rule(premises=['Q'], conclusion='P', rule_id="Cycle Rule 1 (Q -> P)"),
        Rule(premises=['P'], conclusion='Q', rule_id="Cycle Rule 2 (P -> Q)")
    ]
    cyclic_proven, _ = backward_chaining('P', cyclic_rules, set())
    print(f"Result: Cycle safely caught and terminated without infinite loop? -> {not cyclic_proven}")


if __name__ == "__main__":
    main()
