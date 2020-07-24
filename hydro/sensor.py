import fcntl  # used to access I2C parameters like addresses
import time  # used for sleep delay and timestamps
import re


class Sensor:
    def __init__(self):
        self.device = AtlasI2C()  # creates the I2C port object, specify the address or bus if necessary
        self.addresses = self.device.list_i2c_devices()
        self.pH_addr = self.get_pH_address()
        self.EC_addr = self.get_EC_address()
        self.ORP_addr = self.get_ORP_address()
        self.temp_addr = self.get_temp_address()

    def get_pH(self):
        return self._get_reading(self.pH_addr)

    def get_EC(self):
        return self._get_reading(self.EC_addr)

    def get_ORP(self):
        return self._get_reading(self.ORP_addr)

    def get_temp(self):
        return self._get_reading(self.temp_addr)

    def get_pH_address(self):
        return self._get_address("pH")

    def get_EC_address(self):
        return self._get_address("EC")

    def get_ORP_address(self):
        return self._get_address("ORP")

    def get_temp_address(self):
        return self._get_address("RTD")

    def _get_reading(self, address):
        self.device.set_i2c_address(address)
        try:
            return float(self.device.query("R"))
        except ValueError:
            return None

    def _get_address(self, address_string, tries=0):
        if tries == 5:
            raise Exception("Could not find address of type: " + address_string)
        for address in self.addresses:
            self.device.set_i2c_address(address)
            info = self.device.query("I")
            if len(info.split(",")) < 2:
                return self._get_address(address_string, tries=tries + 1)
            else:
                type = info.split(",")[1]
                if type == address_string:
                    return address
        raise Exception("Could not find address of type: " + address_string)


class AtlasI2C:
    long_timeout = 1.5  # the timeout needed to query readings and calibrations
    short_timeout = .5  # timeout for regular commands
    default_bus = 1  # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
    default_address = 98  # the default address for the sensor
    current_addr = default_address

    def __init__(self, address=default_address, bus=default_bus):
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with bus
        # it is usually 1, except for older revisions where its 0
        # wb and rb indicate binary read and write

        self.file_read = open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.file_write = open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # initializes I2C to either a user specified or default address
        self.set_i2c_address(address)

    def set_i2c_address(self, addr):
        # set the I2C communications to the slave specified by the address
        # The commands for I2C dev using the ioctl functions are specified in
        # the i2c-dev.h file from i2c-tools
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
        self.current_addr = addr

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        cmd = cmd.encode()
        self.file_write.write(cmd)

    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C, then parses and displays the result
        response = self.file_read.read(num_of_bytes)  # read from the board
        filtered = bytes(filter(lambda x: x != 0, response))  # remove the null characters to get the response
        if filtered and filtered[0] == 1:  # if the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(x & ~0x80), filtered[1:])
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return ''.join(char_list)  # convert the char list to a string and returns it
        else:
            if filtered:
                return "Error " + str(int(filtered[0]))
            else:
                return 'No response'

    def query(self, string):
        # write a command to the board, wait the correct timeout, and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if string.upper().startswith("R") or string.upper().startswith("CAL"):
            time.sleep(self.long_timeout)
        elif string.upper().startswith("SLEEP"):
            return "sleep mode"
        else:
            time.sleep(self.short_timeout)

        return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close()

    def list_i2c_devices(self):
        prev_addr = self.current_addr  # save the current address so we can restore it after
        i2c_devices = []
        for i in range(0, 128):
            try:
                self.set_i2c_address(i)
                self.read()
                i2c_devices.append(i)
            except IOError as e:
                pass
        self.set_i2c_address(prev_addr)  # restore the address we were using
        return i2c_devices


def main():
    device = AtlasI2C()  # creates the I2C port object, specify the address or bus if necessary

    print(">> Atlas Scientific sample code")
    print(">> Any commands entered are passed to the board via I2C except:")
    print(">>   List lists the available I2C addresses.")
    print(">>   Address,xx changes the I2C address the Raspberry Pi communicates with.")
    print(">>   Poll,xx.x command continuously polls the board every xx.x seconds")
    print(">>   Cal,[high,mid,low],xx.x command calibrates the probe")
    print(" where xx.x is longer than the %0.2f second timeout." % AtlasI2C.long_timeout)
    print(">> Pressing ctrl-c will stop the polling")

    # main loop
    while True:
        console_input = input("Enter command: ")
        if console_input.upper().startswith("LIST"):
            devices = device.list_i2c_devices()
            for i in range(len(devices)):
                print(devices[i])

        # address command lets you change which address the Raspberry Pi will poll
        elif console_input.upper().startswith("ADDRESS"):
            addr = int(console_input.split(',')[1])
            device.set_i2c_address(addr)
            print("I2C address set to " + str(addr))

        # address command lets you change which address the Raspberry Pi will poll
        elif console_input.upper().startswith("CAL"):
            split = console_input.split(',')
            if len(split) == 3:
                point = split[1]
                value = float(split[2])
                response = device.query("cal,%s,%d" % (point, value))
                print(response)
            else:
                response = device.query(console_input.lower())
                print(response)

        # continuous polling command automatically polls the board
        elif console_input.upper().startswith("POLL"):
            delaytime = float(console_input.split(',')[1])

            # check for polling time being too short, change it to the minimum timeout if too short
            if delaytime < AtlasI2C.long_timeout:
                print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
                delaytime = AtlasI2C.long_timeout

            # get the information of the board you're polling
            info = device.query("I").split(",")[1]
            print("Polling %s sensor every %0.2f seconds, press ctrl-c to stop polling" % (info, delaytime))

            try:
                while True:
                    print(device.query("R"))
                    time.sleep(delaytime - AtlasI2C.long_timeout)
            except KeyboardInterrupt:  # catches the ctrl-c command, which breaks the loop above
                print("Continuous polling stopped")

        # if not a special keyword, pass commands straight to board
        else:
            if len(console_input) == 0:
                print("Please input valid command.")
            else:
                try:
                    print(device.query(console_input))
                except IOError:
                    print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")


if __name__ == '__main__':
    main()
