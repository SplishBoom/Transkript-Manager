# transkript-manager

Hi it's Emir writing. 

First of all, this is a kind of management system which only works with the format of MEF University !
|
|__The purpose of this project is to answer questionn of "How would my CPGA will be if I have taken A for a B+ course for example.
|
|__The system is not providing this much info on itself. It only provides the current semester for calculations. 
|
|__However, you can check all of your academical history by this system. (You are welcome)


1-) Important for automatic logings, you can create a json file -> "Sources/payload.json". 
    After that you can fill the file by the format below.
    {
        "username" : "someUserName",
        "password" : "somePassWord",
        "autoLogin" : true
    }
    Note that, you should type right username and password, otherwise it will not login automatically.

2-) You can directly run installRequirements.bat file to upload packages. Or you can use requirements.txt