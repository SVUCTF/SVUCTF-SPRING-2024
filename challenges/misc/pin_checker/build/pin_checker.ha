use bufio;
use fmt;
use os;
use strings;
use time;


export fn main() void = {
	const pin = strings::toutf8(os::getenv("PIN") as str);
	const flag = os::getenv("GZCTF_FLAG") as str;

	fmt::printfln("Please enter your PIN code (N digits):")!;
	const user_pin = bufio::read_line(os::stdin)! as []u8;

	fmt::printfln("Checking PIN...")!;
	if (!equal(pin, user_pin)) {
		fmt::printfln("Access denied.")!;
		return;
	};

	fmt::printfln("Flag: {}", flag)!;
};


fn equal(a: []u8, b: []u8) bool = {
        if (len(a) != len(b)) {
                return false;
        };
        for (let i = 0z; i < len(a); i += 1) {
		time::sleep(time::MILLISECOND * 300);
                if (a[i] != b[i]) {
                        return false;
                };
        };
        return true;
};
