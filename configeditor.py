import json
import re
import requests as r

config = {}
try:
    with open('limiteds.json', 'r') as f:
        config = json.load(f)

    print("Succesfully loaded previous config!")
except FileNotFoundError:
    pass


def new():
    config["cookie"] = input("Full roblox cookie: ")
    config["webhook"] = input("Webhook url: ")
    config['pingall'] = True if input("Ping everyone Y/N: ").lower() == "y" else False

    config['DEBUG_MESSAGES'] = True if input("Do you want to log all gotten prices in the console? Y/N: ").lower() == "y" else False

    config['limiteds'] = []
    for i in range(int(input("Amount of limiteds you want to snipe: "))):
        config["limiteds"].append({})
        asset_id = input(f"{i+1}) The asset id of the limited: ")
        config['limiteds'][i]['asset'] = asset_id

        config['limiteds'][i]['price'] = input(f"{i+1}) Maximum price to pay for the limited: ")
        config['limiteds'][i]['buyagain'] = True if input(
                f"{i+1}) Do you want the limited sniper to buy the item more then once Y/N: ").lower() == 'y' else False


        out  = r.get(f"https://www.roblox.com/catalog/{asset_id}").text
        items = re.compile(r"data-product-id=.*")

        matches = items.finditer(str(out))
        productid = None
        for x in matches:
            productid = str(x.group()[17:].split("\"")[0])


        config['limiteds'][i]["productid"] = productid

        print('\n')


    with open("limiteds.json", 'w') as f:
        json.dump(config, f, indent=4)

    print('Succesfully saved config. You can now close this window')
    input()


def edit():
    while True:
        choice = input("\nWhat do you want to edit.\n"
                       "1) The .ROBLOSECURITY cookie\n"
                       "2) The webhook\n"
                       "3) An asset.\n"
                       "4) Logging information\n"
                       "5) Add an asset to snipe\n"
                       "6) Save and quit\n"
                       "> "
                       )

        if int(choice) == 1:
            config["cookie"] = input("Full roblox cookie: ")

        elif int(choice) == 2:
            config["webhook"] = input("Webhook url: ")
            config['pingall'] = True if input("Ping everyone Y/N: ").lower() == "y" else False

        elif int(choice) == 3:
            asset_id = input("The asset id of the item you want to configure: ")

            item_idx = -1
            for idx, item in enumerate(config['limiteds']):
                if item['asset'] == asset_id:
                    item_idx = idx
                    break

            if item_idx == -1:
                print("asset id doesn't exist. Please check if you've put in a valid id.")
                continue

            config['limiteds'][item_idx]['price'] = input("Maximum price for the limited: ")
            config['limiteds'][item_idx]['buyagain'] = True if input(
                "Do you want to buy the item multiple times Y/N: ").lower() == 'y' else False

        elif int(choice) == 4:
            config['pingall'] = True if input(
                "Do you want to log all gotten prices in the console? Y/N: ").lower() == "y" else False

        elif int(choice) == 5:
            config['limiteds'].append({})

            asset_id = input("The asset id of the limited: ")
            config['limiteds'][-1]['asset'] = asset_id

            config['limiteds'][-1]['price'] = input("Maximum price to pay for the limited: ")
            config['limiteds'][-1]['buyagain'] = True if input(
                "Do you want the limited sniper to buy the item more then once Y/N: ").lower() == 'y' else False

            out = r.get(f"https://www.roblox.com/catalog/{asset_id}").text
            items = re.compile(r"data-product-id=.*")

            matches = items.finditer(str(out))
            productid = None
            for x in matches:
                productid = str(x.group()[17:].split("\"")[0])

            config['limiteds'][-1]["productid"] = productid


        elif int(choice) == 6:
            with open("limiteds.json", 'w') as f:
                json.dump(config, f, indent=4)

            print('Succesfully saved config. You can now close this window')
            input()


def main():
    if config == {}:
        new()
        exit(0)

    choice = input("Welcome to the config editor what do you want to do?\n"
                   "1) Edit existing config\n"
                   "2) Make a new config\n"
                   "> ")

    if int(choice) == 1:
        edit()

    elif int(choice) == 2:
        new()



if __name__ == '__main__':
    main()
