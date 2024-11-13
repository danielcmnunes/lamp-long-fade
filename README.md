# About
The Tapo L510E is a Smart Wi-Fi Dimmable Light Bulb.
It has a nice fade off feature, which has now limit of 30 minutes.

This project allow you to create longer linear fade effects, more natural sunrise/sunset atmospheres.

## How to install
It uses the tapo project (https://pypi.org/project/tapo/) which you can install via:

`pip install tapo
`

## How it Works 
You need to create a credentials.json at the same folder as LampLongFade.py in order to control the lamp, and its home network ip address:

```
{
    "username": "<your tapo username>",
    "password": "<your tapo password>",
    "network_address": "<your lamp local ip>"
}
```

You can specify the starting brightness, the end brightness and the length of the dimming effect in minutes.

Usage examples:<br><br>
`
python LampLongFade.py 100 40
`

Will create a linear fade from lamp's current brightness level to 100 in 40 minutes.

`
python LampLongFade.py 100 20 60
`

Will create a linear fade forcing the lamp to start from a brightness 100 to 20 in 60 minutes.

