import streamlit as st
import copy

def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    newRules = []
    newChar = start_symbol + "'"
    while (newChar in nonterm_userdef):
        newChar += "'"
    
    newRules.append([newChar, ['.', start_symbol]])
    
    for rule in rules:
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

def findClosure(input_state, dotSymbol, separatedRulesList, start_symbol):
    closureSet = []
    
    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        closureSet = input_state
    
    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)
        tempClosureSet = []
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)
        
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet

def compute_GOTO(state, statesDict, separatedRulesList, stateMap, stateCount):
    generateStatesFor = []
    for rule in statesDict[state]:
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)
    
    if len(generateStatesFor) != 0:
        for symbol in generateStatesFor:
            stateCount = GOTO(state, symbol, statesDict, separatedRulesList, stateMap, stateCount)
    return stateCount

def GOTO(state, charNextToDot, statesDict, separatedRulesList, stateMap, stateCount):
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.':
            if rule[1][indexOfDot + 1] == charNextToDot:
                shiftedRule = copy.deepcopy(rule)
                shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
                shiftedRule[1][indexOfDot + 1] = '.'
                newState.append(shiftedRule)
    
    addClosureRules = []
    for rule in newState:
        indexDot = rule[1].index('.')
        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexDot + 1], separatedRulesList, start_symbol)
            for rule in closureRes:
                if rule not in addClosureRules and rule not in newState:
                    addClosureRules.append(rule)
    
    for rule in addClosureRules:
        newState.append(rule)
    
    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break
    
    if stateExists == -1:
        stateCount += 1
        statesDict[stateCount] = newState
        stateMap[(state, charNextToDot)] = stateCount
    else:
        stateMap[(state, charNextToDot)] = stateExists
    return stateCount

def generateStates(statesDict, separatedRulesList, stateMap, stateCount):
    prev_len = -1
    called_GOTO_on = []
    
    while (len(statesDict) != prev_len):
        prev_len = len(statesDict)
        keys = list(statesDict.keys())
        
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                stateCount = compute_GOTO(key, statesDict, separatedRulesList, stateMap, stateCount)
    return stateCount

def first(rule, diction, term_userdef):
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'
    
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            fres = []
            rhs_rules = diction[rule[0]]
            
            for itr in rhs_rules:
                indivRes = first(itr, diction, term_userdef)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)
            
            if '#' not in fres:
                return fres
            else:
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:], diction, term_userdef)
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('#')
                return fres

def follow(nt, start_symbol, rules, diction):
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
                    
                    if len(subrule) != 0:
                        res = first(subrule, diction, term_userdef)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT, start_symbol, rules, diction)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        if nt != curNT:
                            res = follow(curNT, start_symbol, rules, diction)
                    
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)

def createParseTable(statesDict, stateMap, T, NT, separatedRulesList, rules, diction):
    rows = list(statesDict.keys())
    cols = T + ['$'] + NT
    
    Table = []
    tempRow = []
    for y in range(len(cols)):
        tempRow.append('')
    for x in range(len(rows)):
        Table.append(copy.deepcopy(tempRow))
    
    for entry in stateMap:
        state = entry[0]
        symbol = entry[1]
        a = rows.index(state)
        b = cols.index(symbol)
        if symbol in NT:
            Table[a][b] = Table[a][b] + f"{stateMap[entry]} "
        elif symbol in T:
            Table[a][b] = Table[a][b] + f"S{stateMap[entry]} "
    
    numbered = {}
    key_count = 0
    for rule in separatedRulesList:
        tempRule = copy.deepcopy(rule)
        tempRule[1].remove('.')
        numbered[key_count] = tempRule
        key_count += 1
    
    for stateno in statesDict:
        for rule in statesDict[stateno]:
            if rule[1][-1] == '.':
                temp2 = copy.deepcopy(rule)
                temp2[1].remove('.')
                for key in numbered:
                    if numbered[key] == temp2:
                        follow_result = follow(rule[0], start_symbol, rules, diction)
                        for col in follow_result:
                            index = cols.index(col)
                            if key == 0:
                                Table[stateno][index] = "Accept"
                            else:
                                Table[stateno][index] = Table[stateno][index] + f"R{key} "
    
    return Table, cols, rows

# Streamlit app
st.title("SLR(1) Parser Generator")

# Input section
st.header("Grammar Input")
st.write("Enter grammar rules in the format: A -> B | C")

# Initialize session state for rules
if 'rules' not in st.session_state:
    st.session_state.rules = ["E -> E + T | T", "T -> T * F | F", "F -> ( E ) | id"]

# Display rules input
rules = []
for i in range(len(st.session_state.rules)):
    rule = st.text_input(f"Rule {i+1}", value=st.session_state.rules[i], key=f"rule_{i}")
    rules.append(rule)

# # Add/remove rule buttons
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Add Rule"):
#         st.session_state.rules.append("")  # Add a new empty rule
#         # Trigger the rerun by changing the rules list
#         # st.experimental_rerun()  
# with col2:
#     if st.button("Remove Rule") and len(st.session_state.rules) > 1:
#         st.session_state.rules.pop()  # Remove last rule
#         # Trigger the rerun by changing the rules list
#         # st.experimental_rerun() 

# Other inputs
nonterm_userdef = st.text_input("Non-terminal symbols (separated by space)", "E T F").split()
term_userdef = st.text_input("Terminal symbols (separated by space)", "id + * ( )").split()
start_symbol = st.text_input("Start symbol", "E")

if st.button("Generate Parser"):
    st.header("Results")
    
    # Display original grammar
    st.subheader("Original Grammar")
    for rule in rules:
        st.write(rule)
    
    # Grammar augmentation
    separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)
    
    st.subheader("Augmented Grammar")
    for rule in separatedRulesList:
        st.write(f"{rule[0]} -> {' '.join(rule[1])}")
    
    # Initialize variables
    statesDict = {}
    stateMap = {}
    stateCount = 0
    diction = {}
    
    # Calculate closure
    I0 = findClosure(0, start_symbol, separatedRulesList, start_symbol)
    statesDict[0] = I0
    
    st.subheader("Initial Closure (I0)")
    for rule in I0:
        st.write(f"{rule[0]} -> {' '.join(rule[1])}")
    
    # Generate states
    stateCount = generateStates(statesDict, separatedRulesList, stateMap, stateCount)
    # Display generated states
    with st.expander("🔍 View Generated States"):
        for state_num, state_rules in statesDict.items():
            st.markdown(f"**I{state_num}:**")
            for rule in state_rules:
                st.write(f"{rule[0]} -> {' '.join(rule[1])}")


    # Create parsing table
    rules.insert(0, f"{separatedRulesList[0][0]} -> {separatedRulesList[0][1][1]}")
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    
    Table, cols, rows = createParseTable(statesDict, stateMap, term_userdef, nonterm_userdef, separatedRulesList, rules, diction)
    
    # Display parsing table
    st.subheader("SLR(1) Parsing Table")
    
    # Create DataFrame for better display
    import pandas as pd
    df = pd.DataFrame(Table, columns=cols, index=[f"I{i}" for i in rows])
    st.dataframe(df)
