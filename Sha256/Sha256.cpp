/*=============================================================================
* Jonah Ebent, 12/10/2024
* This is an implementation of the SHA-256 hash algorithm according to the
* NIST.FIPS 180-4 specifications.
*   https://csrc.nist.gov/groups/ST/toolkit/secure_hashing.html
*   https://csrc.nist.gov/groups/ST/toolkit/examples.html
* I used this website in order to validate that my hashes were correct.
*   https://www.movable-type.co.uk/scripts/sha256.html 
=============================================================================*/
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;
typedef uint32_t word;
typedef vector<word> block;

class Sha256 {
public:
    static string hash(string msg) {
        // SHA-256 constants defined in [§4.2.2]
        const vector<word> K = {
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        };

        // §5: Preprocessing
        pad(msg);
        vector<block> M = parse(msg);

        // Initial hash value defined in [§5.3.3]
        vector<word> H = {
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        };
        
        // §6.2.2 Hash Computation
        for (block M : M) {
            vector<word> W(64);             // block-specific message schedule
            prepareMessageSchedule(M, W);
            word a = H[0];
            word b = H[1];
            word c = H[2];
            word d = H[3];
            word e = H[4];
            word f = H[5];
            word g = H[6];
            word h = H[7];
            for (int t = 0; t < 64; t++) {
                word T1 = h + SIGMA_1(e) + Ch(e, f, g) + K[t] + W[t];
                word T2 = SIGMA_0(a) + Maj(a, b, c);
                h = g;
                g = f;
                f = e;
                e = d + T1;
                d = c;
                c = b;
                b = a;
                a = T1 + T2;
            }
            H[0] += a;
            H[1] += b;
            H[2] += c;
            H[3] += d;
            H[4] += e;
            H[5] += f;
            H[6] += g;
            H[7] += h;
        }

        // Return value as hex string
        stringstream ss;
        for (int i = 0; i < 8; i++) {
            ss << hex << setw(8) << setfill('0') << H[i];
        }
        return ss.str();
    }

private:
    // Shift operations defined in [§3.2]
    static word shr(word x, uint8_t n) { return x >> n; }
    static word rotr(word x, uint8_t n) { return (x >> n) | (x << (32 - n)); }

    // 6 logical functions defined in [§4.1.2]

    // Choose: result bit comes from y if x bit is 0 and z if x bit is 1
    static word Ch(word x, word y, word z) { return (x & y) ^ (~x & z); }
    // Majority: result bit is the majority of the three input bits
    static word Maj(word x, word y, word z) { return (x & y) ^ (x & z) ^ (y & z); }
    static word SIGMA_0(word x) { return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22); }
    static word SIGMA_1(word x) { return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25); }
    static word sigma_0(word x) { return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3); }
    static word sigma_1(word x) { return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10); }

    // Pads the message to a multiple of 512 bits, as defined in [§5.1.1]
    static void pad(string& msg) {
        size_t l = msg.length() * 8;
        size_t k = (448 - l - 1) % 512;
        msg += '\x80';
        msg.append(k / 8, '\0');
        for (int i = 0; i < 64; i += 8) {
            msg += static_cast<char>((l >> (56 - i)) & 0xff);
        }
    }

    // Parses the message into N 512-bit blocks [§5.2.1], where:
    //  - N is the size of the return value
    //  - each block is represented as a vector of 16 32-bit words
    static vector<block> parse(const string& msg) {
        vector<block> blocks = {};
        for (size_t i = 0; i < msg.length(); i += 64) {
            block b = {};
            for (size_t j = 0; j < 64; j += 4) {
                word w = 0;
                for (size_t k = 0; k < 4; k++) {
                    unsigned char c = msg[i + j + k];
                    w = (w << 8) | c;
                }
                b.push_back(w);
            }
            blocks.push_back(b);
        }
        return blocks;
    }

    // Populates the message schedule W according to [§6.2.2]
    static void prepareMessageSchedule(const block &M, vector<word> &W) {
        for (size_t t = 0; t < 64; t++) {
            if (t <= 15) {
                W[t] = M[t];
            }
            else {
                W[t] = sigma_1(W[t - 2]) + W[t - 7] + sigma_0(W[t - 15]) + W[t - 16];
            }
        }
    }
};


int main() {
    while (true) {
        string msg;
        cout << "Enter a string to hash (or q to quit): ";
        getline(cin, msg);
        if (msg == "q") break;
        cout << "The SHA-256 hash of \"" << msg << "\" is " << Sha256::hash(msg) << endl;
        cout << endl;
    }
}