import json

def decode_json_file(filename):
    with open(filename, 'r', encoding='latin1') as file:
        data = json.load(file)

    return data

def encode_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    input_filename = 'processed_fixed_merged.json'
    output_filename = 'new_merged.json'

    decoded_data = decode_json_file(input_filename)

    encode_json_file(decoded_data, output_filename)

    print(f"Decoded text has been saved to {output_filename}")

if __name__ == "__main__":
    main()
