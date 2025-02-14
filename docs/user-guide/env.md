# The .env File

Many apps and software store data related to its current environment in a file called *.env*. Data can be stored in Key-Value pairs, like this:


```json
VARIABLE="value!"
```
This is a powerful capability -- it allows apps to provide a convenient way to configure their own instance without shipping secrets in production! In other words, it keeps developers from accidentally putting their passwords on the internet. GroundStatation also uses an environment variable (not to be confused with a shell environment variable) to store its password! 
  

Python can read these environment files using these functions:

```python
load_dotenv()
os.getenv("<variable-name-here")
```

More information on these methods can be found [here!](https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/#)

FlightControl uses variables defined in this way to store other options about its runtime configuration. Many are only used for testing or developer usage, but there are some that most users will probably need to set and few that are *required* for using FlightControl. 

## Sensible Defaults
FlightControl will eventually ship with a .env file with *sensible defaults*. When determining the sensible defaults, we assumed a few things:

- Most users are using in the intended way
- Most users don't have extenuating setup circumstances
- Most users aren't interested in extra tinkering

::: info
FlightControl **won't** ever ship with a default password. Because it is connected to a rocket, we take the security of our application during runtime seriously. Don't worry -- the passcode is set very quickly in the default [install process.](installation.md)
:::

With these assumptions in mind, the sensible defaults only really set two things:

- The default serial port is set to the default Raspberry Pi USB serial port. 
- The app is configured to run on real hardware tracking a rocket -- not a development environment.

If these defaults don't fit your needs, be sure to keep reading and check out all of the configuration options you can use out of the box. If there is a feature you need for your team to succeed, make an issue on [GitHub](https://www.github.com/nathansamuell/FlightControl/issues) or fork the project to hack on and check out the [Developer Reference](../developer-reference/dev-landing.md).

## FlightControl's .env Variables
Below is a [table](#table-1) of all currently configureable .env variables. Some variables are **required** for FlightControl to work properly. Sensible defaults are setup in the [install instructions](installation.md) Some variables are used only in development or testing. They are included here in case they are useful for troubleshooting your own installation or customizing for your own situation. More information about developer variables can be found [here](../developer-reference/dev-landing.md)

### Table 1
|    Name                                          | Required | Developer | Default included? |    Type     |
|  :--------:                                      | :------: | :-------: | :---------------: |  :------:   |
| [USER_PASS](#env-variable-user_pass)             |     *    |           |        no         | string/int  |
| [SERIAL_PORT](#env-variable-serial_port)         |     *    |           |        yes        |   string    |
| [MOCK_SERIAL](#env-variable-mock_serial)         |     *    |      *    |        yes        | bool/string |
| [MOCK_SPORT_GS](#env-variable-mock_sport_gs)     |          |      *    |        no         |   string    |
| [MOCK_SPORT_TEST](#env-variable-mock_sport_test) |          |      *    |        no         |   string    |



### .env variable: USER_PASS
  
* [x] Required
* [ ] Developer
* [ ] Set By Default
  
This variable is a string representation of a numerical passcode for FlightControl. It can be however many digits you desire.

Sample Setting:

```json
USER_PASS="123456"
```
This number will be converted to an integer under the hood and compared against what the user enters logging in. Without logging in, you cannot establish communication to a rocket. 

### .env variable: SERIAL_PORT

* [ ] Required
* [ ] Developer
* [x] Set By Default

This variable holds the filepath of the serial port that FlightControl expects to read rocket data from. It is not techically required in a testing setting (see [MOCK_SPORT_GS](#env-variable-mock_sport_gs)), but it is configured by default because the target machine **NEEDS** it during launch.

Sample Setting:
```json
SERIAL_PORT="/dev/ttyUSB0"
```

### .env variable: MOCK_SERIAL

* [x] Required
* [x] Developer
* [x] Set By Default

This variable is a boolean represented by a string ```"True"``` or ```"False"```.

### .env variable: MOCK_SPORT_GS
* [ ] Required
* [x] Developer
* [ ] Set By Default

This is a developer variable to enable local testing on one machine. Provided you can configure the serial port communication on your machine, you should create a pair of virtual serial porst and assign one to this variable. This is the port that FlightControl listens to, but the assignment is arbitrary.

### .env variable: MOCK_SPORT_TEST

* [ ] Required
* [x] Developer
* [ ] Set By Default

This is the other serial port in the pair -- this port is the one that the simulator program sends data to. 