import re 

def check_mask_regex(serial_num: str, mask_sn: str) -> bool:
    '''Validation of the mask for compliance'''
    if len(serial_num) != len(mask_sn):
        return {"message": "Does not match the mask"} 
    
    regx = {
        "N": "[0-9]",
        "A": "[A-Z]",
        "a": "[a-z]",
        "X": "[A-Z0-9]",
        "Z": "[-|_|@]"
    }
    
    x = ''
    
    for sym in mask_sn:
        x += regx[sym]  

    result = re.fullmatch(rf"{x}", rf"{serial_num}") 

    return True if result else {"message": "Does not match the mask"}
