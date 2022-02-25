import usb_hid

print("SETTING UP PP_GENERIC USB HID")
print("1/30/2022 1000")
# This is only one example of a gamepad descriptor, and may not suit your needs.

PP_GENERIC_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,                     # USAGE_PAGE (Generic Desktop)
    0x09, 0x05,                     # USAGE (Game Pad)
    0xa1, 0x01,                     # COLLECTION (Application)
    0xa1, 0x00,                     #   COLLECTION (Physical)
    0x85, 0x01,                     #     REPORT_ID (1)
    0x05, 0x09,                     #     USAGE_PAGE (Button)
    0x19, 0x01,                     #     USAGE_MINIMUM (Button 1)
    0x29, 0x20,                     #     USAGE_MAXIMUM (Button 32)
    0x15, 0x00,                     #     LOGICAL_MINIMUM (0)
    0x25, 0x01,                     #     LOGICAL_MAXIMUM (1)
    0x75, 0x01,                     #     REPORT_SIZE (1)
    0x95, 0x20,                     #     REPORT_COUNT (32)
    0x81, 0x02,                     #     INPUT (Data,Var,Abs)
    0xc0,                           #   END_COLLECTION
    0xc0,                           # END_COLLECTION
    0x05, 0x01,                     # USAGE_PAGE (Generic Desktop)
    0x09, 0x05,                     # USAGE (Game Pad)
    0xa1, 0x01,                     # COLLECTION (Application)
    0xa1, 0x00,                     #   COLLECTION (Physical)
    0x85, 0x02,                     #   REPORT_ID (2)
    0x05, 0x01,                     #   Usage Page (Generic Desktop Ctrls)
    0x09, 0x30,                     #   Usage (X)
    0x09, 0x31,                     #   Usage (Y)
    0x09, 0x32,                     #   Usage (Z)
    0x09, 0x33,                     #   Usage (Rx)
    0x09, 0x34,                     #   Usage (Ry)
    0x09, 0x35,                     #   Usage (Rz)
    0x09, 0x36,                     #   Usage (Slider)
    0x09, 0x36,                     #   Usage (Slider)
    0x15, 0x81,                     #   Logical Minimum (-127)
    0x25, 0x7F,                     #   Logical Maximum (127)
    0x75, 0x08,                     #   Report Size (8)
    0x95, 0x08,                     #   Report Count (8)
    0x81, 0x02,                     #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xc0,                           #   END_COLLECTION
    0xc0,                           # END_COLLECTION
))

gamepad = usb_hid.Device(
    report_descriptor=PP_GENERIC_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(1,2,),           # Descriptor uses report ID 4.
    in_report_lengths=(4,8,),    # This gamepad sends 6 bytes in its report.
    out_report_lengths=(0,0,),   # It does not receive any reports.
)

usb_hid.enable((gamepad,))

print("hid_descriptor:")
for b in PP_GENERIC_REPORT_DESCRIPTOR:
    print("{:02x}".format(b))
print("DONE")

