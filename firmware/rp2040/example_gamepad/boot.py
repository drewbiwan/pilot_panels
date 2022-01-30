import usb_hid

print("SETTING UP PP_GENERIC USB HID")
print("1/30/2022 1000")
# This is only one example of a gamepad descriptor, and may not suit your needs.

PP_GENERIC_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  #  Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  #  Usage (Gamepad)
    0xA1, 0x01,  #  Collection (Application)
    0xA1, 0x00,  #      Collection (Physcial)
    0x05, 0x09,  #          Usage Page (Button)
    0x19, 0x01,  #          Usage Minimum (Button 1)
    0x29, 0x20,  #          Usage Maximum (Button 32)
    0x15, 0x00,  #          Logical Minimum (0)
    0x25, 0x01,  #          Logical Maximum (1)
    0x75, 0x01,  #          Report Size (1)
    0x95, 0x20,  #          Report Count (32)
    0x81, 0x02,  #          Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        #      End Collection
    0xC0,        #  End Collection
))


"""
    0x85, 0x01,  #          Report ID (1)

0x05, 0x01,  #      Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  #      Usage (Gamepad)
    0xA1, 0x00,  #      Collection (Physcial)
    0x85, 0x02,  #          Report ID (2)
    0x05, 0x01,  #          Usage Page (Generic Desktop Ctrls)
    0x15, 0x81,  #          Logical Minimum (-127)
    0x25, 0x7F,  #          Logical Maximum (127)
    0x09, 0x30,  #          Usage (X)
    0x09, 0x31,  #          Usage (Y)
    0x09, 0x32,  #          Usage (Z)
    0x09, 0x33,  #          Usage (Rx)
    0x09, 0x34,  #          Usage (Ry)
    0x09, 0x35,  #          Usage (Rz)
    0x75, 0x08,  #          Report Size (8)
    0x95, 0x06,  #          Report Count (6)
    0x81, 0x02,  #          Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        #      End Collection


0x40, 0x0A,  #   Usage Page (Ordinals)
0x19, 0x01,  #      Usage Minimum (Instance 1)
0x29, 0x08,  #      Usage Maximum (Instance 8)
0x15, 0x81,  #      Logical Minimum (-127)
0x25, 0x7F,  #      Logical Maximum (127)
0x75, 0x08,  #      Report Size (8)
0x95, 0x08,  #      Report Count (8)
0x81, 0x02,  #      Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
"""

gamepad = usb_hid.Device(
    report_descriptor=PP_GENERIC_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(1,),           # Descriptor uses report ID 4.
    in_report_lengths=(4,),    # This gamepad sends 6 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     gamepad)
)


print("DONE")

