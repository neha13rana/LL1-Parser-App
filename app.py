import streamlit as st
import pandas as pd

rules = []
nonterm_userdef = []
term_userdef = []
diction = {}
firsts = {}
follows = {}
start_symbol = None

def removeLeftRecursion(rulesDiction):
    store = {}
    for lhs in rulesDiction:
        alphaRules = []
        betaRules = []
        allrhs = rulesDiction[lhs]
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        if len(alphaRules) != 0:
            lhs_ = lhs + "'"
            while lhs_ in rulesDiction.keys() or lhs_ in store.keys():
                lhs_ += "'"
            for b in range(len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDiction[lhs] = betaRules
            for a in range(len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['#'])
            store[lhs_] = alphaRules
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction

def LeftFactoring(rulesDiction):
    newDict = {}
    for lhs in rulesDiction:
        allrhs = rulesDiction[lhs]
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        new_rule = []
        tempo_dict = {}
        for term_key in temp:
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                lhs_ = lhs + "'"
                while lhs_ in rulesDiction.keys() or lhs_ in tempo_dict.keys():
                    lhs_ += "'"
                new_rule.append([term_key, lhs_])
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                new_rule.append(allStartingWithTermKey[0])
        newDict[lhs] = new_rule
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict

def first(rule):
    global term_userdef, diction
    if not rule:
        return ['#']
    if rule[0] in term_userdef:
        return [rule[0]]
    elif rule[0] == '#':
        return ['#']
    
    if rule[0] in diction:
        fres = []
        rhs_rules = diction[rule[0]]
        for itr in rhs_rules:
            indivRes = first(itr)
            if indivRes:
                fres.extend(indivRes)
        
        if '#' in fres and len(rule) > 1:
            fres.remove('#')
            ansNew = first(rule[1:])
            if ansNew:
                fres.extend(ansNew)
        return list(set(fres))
    return []

def follow(nt):
    global start_symbol, diction
    solset = set()
    if nt == start_symbol:
        solset.add('$')
    
    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    if subrule:
                        res = first(subrule)
                        if '#' in res:
                            res.remove('#')
                            if nt != curNT:
                                follow_res = follow(curNT)
                                if follow_res:
                                    res.extend(follow_res)
                        solset.update(res)
                    else:
                        if nt != curNT:
                            follow_res = follow(curNT)
                            if follow_res:
                                solset.update(follow_res)
    return list(solset)

def computeAllFirsts():
    global firsts, diction
    firsts.clear()
    for y in diction:
        firsts[y] = set()
        for sub in diction[y]:
            result = first(sub)
            if result:
                firsts[y].update(result)

def computeAllFollows():
    global follows, diction
    follows.clear()
    for NT in diction:
        follows[NT] = set(follow(NT))

def createParseTable():
    global diction, term_userdef, firsts, follows
    
    parse_table = {}
    for non_term in diction:
        parse_table[non_term] = {}
        for term in term_userdef + ['$']:
            parse_table[non_term][term] = ""
    
    grammar_is_LL = True
    
    for non_term in diction:
        for production in diction[non_term]:
            first_set = first(production)
            
            if '#' in first_set:
                first_set.remove('#')
                follow_set = follows[non_term]
                first_set.extend(follow_set)
            
            for terminal in first_set:
                if terminal in term_userdef + ['$']:
                    if parse_table[non_term][terminal] == "":
                        parse_table[non_term][terminal] = production
                    else:
                        grammar_is_LL = False
    
    return parse_table, grammar_is_LL

def validateStringUsingStackBuffer(parse_table, input_string, start_sym):
    """Validates a string using the parsing table"""
    # Initialize stack and input buffer
    stack = [start_sym, '$']
    input_tokens = input_string.split()
    input_tokens.append('$')
    buffer = input_tokens
    
    steps = []
    steps.append(("Initial Configuration:", f"Stack: {stack}", f"Input: {buffer}"))
    
    while stack and buffer:
        top_stack = stack[0]
        current_input = buffer[0]
        
        steps.append(("Current Step:", f"Stack Top: {top_stack}", f"Current Input: {current_input}"))
        
        if top_stack == current_input:
            stack.pop(0)
            buffer.pop(0)
            steps.append(("Action:", "Matched and consumed terminal", f"Remaining Input: {buffer}"))
        elif top_stack in parse_table:
            if current_input in parse_table[top_stack]:
                production = parse_table[top_stack][current_input]
                if production:
                    # Pop the non-terminal
                    stack.pop(0)
                    # Push the production in reverse (if it's not epsilon)
                    if production != ['#']:
                        stack = production + stack
                    steps.append(("Production Applied:", f"{top_stack} -> {' '.join(production) if production else '#'}", 
                                f"New Stack: {stack}"))
                else:
                    return False, steps, f"No production for {top_stack} with input {current_input}"
            else:
                return False, steps, f"Input symbol {current_input} not in parse table for {top_stack}"
        else:
            return False, steps, f"Unexpected symbol {top_stack} on stack"
    
    if len(stack) <= 1 and len(buffer) <= 1:
        return True, steps, "String accepted!"
    else:
        return False, steps, "String rejected - incomplete parse"

# Streamlit UI
st.title("LL(1) Grammar Analyzer")

# Session state initialization
if 'test_strings' not in st.session_state:
    st.session_state.test_strings = []
if 'parse_table' not in st.session_state:
    st.session_state.parse_table = None
if 'grammar_processed' not in st.session_state:
    st.session_state.grammar_processed = False

# Input section
st.header("Grammar Input")
start_symbol = st.text_input("Enter Start Symbol:", "S")

with st.expander("Enter Grammar Rules", expanded=True):
    num_rules = st.number_input("Number of Rules:", min_value=1, value=4)
    rules = []
    for i in range(num_rules):
        rule = st.text_input(f"Rule {i+1} (format: A -> B c | d)", key=f"rule_{i}")
        if rule:
            rules.append(rule)

nonterm_input = st.text_input("Enter Non-terminals (comma-separated):", "S,A,B,C")
term_input = st.text_input("Enter Terminals (comma-separated):", "a,b,c,d,k,r,O")

# Process Grammar Button
if st.button("Process Grammar"):
    st.session_state.grammar_processed = False
    
    # Clear previous data
    diction.clear()
    nonterm_userdef = [x.strip() for x in nonterm_input.split(',') if x.strip()]
    term_userdef = [x.strip() for x in term_input.split(',') if x.strip()]
    
    # Process rules
    for rule in rules:
        if '->' in rule:
            lhs, rhs = rule.split("->")
            lhs = lhs.strip()
            rhs_parts = [x.strip().split() for x in rhs.split("|")]
            diction[lhs] = rhs_parts
    
    # Grammar Processing
    st.subheader("Grammar Analysis")
    
    with st.expander("Grammar Transformations", expanded=True):
        st.write("After removing left recursion:")
        diction = removeLeftRecursion(diction)
        st.write(diction)
        
        st.write("After left factoring:")
        diction = LeftFactoring(diction)
        st.write(diction)
    
    # Compute FIRST and FOLLOW sets
    computeAllFirsts()
    computeAllFollows()
    
    with st.expander("FIRST and FOLLOW Sets", expanded=True):
        st.write("FIRST Sets:", {k: list(v) for k, v in firsts.items()})
        st.write("FOLLOW Sets:", {k: list(v) for k, v in follows.items()})
    
    # Create parse table
    parse_table, grammar_is_LL = createParseTable()
    st.session_state.parse_table = parse_table
    
    # Display parse table
    st.subheader("Parse Table")
    df_data = []
    terminals = term_userdef + ['$']
    
    for non_term in parse_table:
        row = [non_term]
        for term in terminals:
            production = parse_table[non_term].get(term, "")
            if production:
                row.append(' '.join(production))
            else:
                row.append("")
        df_data.append(row)
    
    df = pd.DataFrame(df_data, columns=['Non-Terminal'] + terminals)
    st.dataframe(df)
    
    if grammar_is_LL:
        st.success("This grammar is LL(1)!")
    else:
        st.error("This grammar is not LL(1)!")
    
    st.session_state.grammar_processed = True

# String Validation Section
if st.session_state.grammar_processed:
    st.header("String Validation")
    
    # Input for new test string
    col1, col2 = st.columns([3, 1])
    with col1:
        new_string = st.text_input("Enter a string to test (space-separated):")
    with col2:
        if st.button("Add String"):
            if new_string and new_string not in st.session_state.test_strings:
                st.session_state.test_strings.append(new_string)
    
    # Display and validate all test strings
    if st.session_state.test_strings:
        st.subheader("Test Results")
        for test_string in st.session_state.test_strings:
            with st.expander(f"String: {test_string}", expanded=True):
                is_valid, steps, message = validateStringUsingStackBuffer(
                    st.session_state.parse_table, test_string, start_symbol)
                
                # Display result
                if is_valid:
                    st.success(message)
                else:
                    st.error(message)
                
                # Display parsing steps
                st.write("Parsing Steps:")
                for i, (step_type, *step_details) in enumerate(steps, 1):
                    st.text(f"Step {i}:")
                    st.text(f"  {step_type}")
                    for detail in step_details:
                        st.text(f"  {detail}")
        
        # Option to clear test strings
        if st.button("Clear All Test Strings"):
            st.session_state.test_strings = []
            st.experimental_rerun()
else:
    st.info("Please process the grammar first before testing strings.")

# Help section
with st.expander("Help & Instructions"):
    st.markdown("""
    ### How to use this LL(1) Grammar Analyzer:
    
    1. **Enter the Grammar**:
       - Specify the start symbol
       - Enter the grammar rules in the format: A -> B c | d
       - List all non-terminals and terminals
    
    2. **Process the Grammar**:
       - Click "Process Grammar" to analyze the grammar
       - View the transformed grammar, FIRST/FOLLOW sets, and parse table
    
    3. **Test Strings**:
       - Enter strings to test in the validation section
       - Add multiple strings to test
       - View detailed parsing steps for each string
    
    ### Example Grammar:
    ```
    S -> A k O
    A -> A d | a B | a C
    C -> c
    B -> b B C | r
    ```
    
    ### Example Test Strings:
    - a r k O
    - a c k O
    - a b r c k O
    """)