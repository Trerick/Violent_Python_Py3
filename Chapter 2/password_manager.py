#Additional task to create a password manager to store, create new, and test pws

class Password_manager:
    
    def __init__(user):
        user.oldPass = []
        
    def set_password(user):
        newPass = input("Enter a new password: ")
        while newPass in user.oldPass:
            newPass = input("Password already exists, enter a new password: ")
        else:
            user.oldPass.append(newPass)
            currentPass = newPass
            print("Your new password is set.")
            return currentPass
                
    def get_password(user):
        return user.oldPass[-1]
    
    def is_correct(user):
        correctPass = input("Enter your current password: ")
        while correctPass != user.get_password():
            print(False, "Incorrect password.")
            correctPass = input("Enter your current password: ")
        else:
            return print(True, "Welcome.")
        
            

manager = Password_manager()
manager.oldPass = ['password', 'admin', '12345']


manager.set_password()
manager.is_correct()
