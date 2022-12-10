file = open("C:\\Users\\Alex Dai\\Documents\\octopath_modding\\Enemy\\Enemy\\EnemyID.uexp", 'rb', buffering=100)
format = ['m_Label', 'm_TypeID', 'm_DisplayLevel', 'm_BreakRate', 'm_MaxSLD', 'm_MaxHP', 'm_MaxSP', 'm_AtkP', 'm_DefP', 'm_AtkM', 'm_DefM', 'm_Agi', 'm_Crt', 'm_CrtDef', 'm_EquipAtk', 'm_ResistAilmentID', 'm_ResistAilment', 'm_TacticalAssignID', 'm_SkillsID', 'm_Exp', 'm_Money', 'm_DropReward', 'm_EventDropRewards', 'm_StatusOffset', 'm_Bottle', 'm_Name', 'm_Level', 'm_Hp', 'm_Shield','m_RaceIndices','m_DisplaySpecialSkillGauge','m_GenerateSpecialSkillValueOrverTurn','m_ReduceSpecialSkillValueBreak','m_MaxSpecialSkillValue','m_id']
type_dict = {
    'm_Label' : 'str', 
    'm_TypeID' : 'hex', 
    'm_DisplayLevel' : 'lvl', 
    'm_BreakRate' : 'hex', 
    'm_MaxSLD' : 'int',
    'm_MaxHP' : 'int', 
    'm_MaxSP' : 'int', 
    'm_AtkP' : 'int', 
    'm_DefP' : 'int', 
    'm_AtkM' : 'int', 
    'm_DefM' : 'int', 
    'm_Agi' : 'int', 
    'm_Crt' : 'int', 
    'm_CrtDef' : 'int', 
    'm_EquipAtk' : 'hex', 
    'm_ResistAilmentID' : 'int', 
    'm_ResistAilment' : 'hex', 
    'm_TacticalAssignID': 'int', 
    'm_SkillsID' : 'int', 
    'm_Exp' : 'int', 
    'm_Money' : 'int', 
    'm_DropReward' : 'hex', 
    'm_EventDropRewards' : 'hex', 
    'm_StatusOffset' : 'hex', 
    'm_Bottle' : 'int', 
    'm_Name' : 'hex', 
    'm_Level' : 'hex', 
    'm_Hp' : 'hex', 
    'm_Shield' : 'hex',
    'm_RaceIndices' : 'hex',
    'm_DisplaySpecialSkillGauge' : 'hex',
    'm_GenerateSpecialSkillValueOrverTurn': 'hex',
    'm_ReduceSpecialSkillValueBreak': 'hex',
    'm_MaxSpecialSkillValue':'hex',
    'm_id' : 'int'
}
out_file = open('octopath_datamine.csv', 'w')

for word in format:
    out_file.write(word + ',')

isbird =False
format.reverse()
word_queue = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA'
value = b'\00'
i = 0
last_word = ''
#try:
while file.readable():
    current_word = format.pop()
    format.insert(0,current_word)
    if last_word == 'm_Label':
        out_file.write('\n')
    while word_queue[-len(current_word):] != current_word:
        byte = file.read(1)
        word_queue += str(byte.decode("ISO-8859-1"))
        if last_word != '':
            value += byte
    if last_word != '':
        value = value[1:-(len(current_word)+1)]
        if type_dict[last_word] == 'str':
            if value[0:1] != b'\xDA':
                out_file.write(str(value[1:].decode("ISO-8859-1")) + ',')
            else:
                out_file.write(str(value[3:].decode("ISO-8859-1")) + ',')
            if 'PRE_AB02_03_01' in str(value.decode("ISO-8859-1")): isbird = True # isbird check
        elif type_dict[last_word] == 'lvl':
            out_file.write(str(value[1:].decode("ISO-8859-1")) + ',')
        elif type_dict[last_word] == 'int':
            if value[0:1] == b'\xd1' or value[0:1] == b'\xd2':
                out_file.write(str(int.from_bytes(value[1:], "big")) + ',')
            else:
                out_file.write(str(int.from_bytes(value, "little")) + ',')
        elif type_dict[last_word] == 'hex':
            out_file.write(value.hex() + ',')
        if isbird and i < len(format):
            print(last_word + ": " + value.hex() + ", " + value.decode('ISO-8859-1'))
            i+=1
        if last_word == 'm_Label': print('Current Enemy: '+value[1:].decode("ISO-8859-1"))
        value = b'\00'
        if len(word_queue) > 1000:
            out_file.flush()
            word_queue = word_queue[-50:]
    last_word = current_word
#except Exception as e:
#    print(e)
#    out_file.flush()
#    out_file.close()
#    print('end')
out_file.flush()
out_file.close()
print('end')