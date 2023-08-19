As of 2023-08-12 (release build)

`Atlas Fallen/build_info`: `* Era - PC 110045 (SVN) / 1691132679 (Git) / 643 - Fri Aug 04 09:49:21 2023`

le/be: Little/Big Endian

## Base Header
Absolute position: 0

- +0: uint32_t le magic - for Atlas Fallen 0x7A145F28
- +4: uint32_t le checksum - over the decompressed Body (see section below for algorithm)
- +8: uint32_t le header_size

## Header (metadata)
Absolute position: 0xC. Length seemingly hardcoded in engine to 0xD0. 

- +0: uint32_t le fledge_body_format - body file format, known 0x29

Other fields not analyzed so far. Appears to contain Name32 fields for 

## Body block header
Absolute position: sizeof(BaseHeader) + BaseHeader.header_size

- +0: bool is_compressed, stored as uint32_t le 
- +4: uint32_t le compressed_size
- +8: uint32_t le decompressed_size

Followed by Body, either raw (`decompressed_size` bytes) or Deflate compressed (`compressed_size` bytes), indicated by `is_compressed`.

## Body

The Body uses _big endian_ encoding for all fields. See the section below for the encoding of the data types.

(Fledge::Core::SaveGameDesc)

- `Name32`
- `Name32`
- `string` (known: "ERA-Savegame")
- `uint32_t` core_body_format - known value 2
- `uint8_t`
- `uint64_t`
- if core_body_format < 1: `uint16_t`
- `bool`
- if core_body_format >= 2: `uint32_t` some\_field1
- `uint32_t` sizevar_1
- for i in range(sizevar_1): {`uint64_t`, `bool`}
- `uint32_t` num_running_conversations
- for i in range(num_running_conversations): {`Name32`, `int32_t`}
- `uint32_t` sizevar_3
- for i in range(sizevar_3): {`Name32`, `bool`}
- `uint32_t` json_string_size
- `binary`, size given by json_string_size.

(Era::SaveGameDesc)

- (all of the above)
- `binary`, size 0x60
- `uint32_t` sizevar_4
- for i in range(sizevar_4): {`uint64_t`, `uint8_t`}
- `uint32_t` sizevar_5
- for i in range(sizevar_5): {`Name32`, for k in range(0x10000): `uint32_t`}
  - data appears to be a raw image; example values for the Name32 field: `hash("__default")=0x2db22441`, `hash("ui_map_lvl2")=0x4f4f451e`
- `Name32` - example: `hash("ui_map_lvl2")=0x4f4f451e`
- `vec3` player position(?)
- `float`
- `bool` boolvar1
- `bool` boolvar2
- `bool` boolvar3
- `bool` boolvar4
- `bool` boolvar5
- if (header.fledge_body_format >= 0x27) `bool` boolvar6
- if (header.fledge_body_format >= 0x28) `bool` boolvar7
- if (header.fledge_body_format >= 0x28) `bool` boolvar8
- if (header.fledge_body_format >= 0x28) `bool` boolvar9
- if (header.fledge_body_format >= 0x28) `bool` boolvar10
- `bool` boolvar11
- `bool` boolvar12
- `uint8_t`
- `bool` boolvar13
- `uint8_t`
- `bool` boolvar14
- `uint8_t`
- if (header.fledge_body_format >= 0x28) `int32_t`
- if (header.fledge_body_format < 0x29) `uint32_t` - apparently moved since format 0x29, same as some\_field1 in core_body_format >= 2
- `uint32_t` sizevar_6
- for i in range(sizevar_6): `uint32_t`
- `uint32_t` sizevar_7
- for i in range(sizevar_7): `uint32_t`
- if (header.fledge_body_format >= 0x18):
  - `uint32_t` sizevar_8
  - for i in range(sizevar_8): `Name32`
- `uint32_t` sizevar_9
- `binary`, size from sizevar_9
- if (header.fledge_body_format >= 0x1B):
  - `uint32_t` sizevar_10
  - for i in range(sizevar_10): `Name32`
- if (header.fledge_body_format >= 0x25):
  - `uint32_t` global_mapdata1
  - `uint32_t` global_mapdata_count
  - for i in range(global_mapdata_count):
    - `uint8_t`
    - `uint8_t`
    - `Variant`
    - `Variant`
    - `Variant`
    - `vec<3>`

### Data types

- Variant
  - 4 byte uint32_t - variant type
    ```
	switch (type) { //each variant type is encoded as specified in the data types list
	  case 1: bool
	  case 2: int32_t
	  case 3: int8_t
	  case 4: uint8_t
	  case 5: uint16_t
	  case 6: uint32_t
	  case 7: uint64_t
	  case 8: float
	  case 9: Degree
	  case 10: Radian
	  case 11: vec<2>
	  case 12: vec<3>
	  case 13: vec<4>
	  case 14: Color
	  case 15: Rotate
	  case 16: quat
	  case 17: UDim
	  case 18: UVector2
	  case 19: Rect
	  case 20: Name32
	  case 21: Ref
	  case 22: (none) //unsure if void or null
	  case 23: Variant array - `uint32_t` count, for i in range(count): `Variant`
	  case 24: Variant dictionary - `uint32_t` count, for i in range(count): `Name32`, `Variant`
	  case 25: Curve
	  default: //void
	}
    ```
- Ref
  - `uint32_t`
  - `uint64_t`
  - `bool`
  - if (\<unknown condition\>) `string`
- Curve
  - `uint32_t` count
  - for i in range(count): `float`, `vec<2>`, `vec<2>`, `vec<2>`
- Rect
  - 2x `uint16_t`
- Color
  - 4x `float`
- Degree
  - `float`
- Radian
  - `float`
- Rotate
  - 3x `Radian`
- quat
  - 4x `float`
- int32_t (4 bytes, be)
- bool (4 bytes (! unlike uint8_t), be) - 0x00000000 (false) or 0x00000001 (true)
- float (4 bytes, be)
- UDim
  - 2x `float`
- UVector2
  - 2x `UDim`
- vec<2>
  - 2x `float`
- vec<3>
  - 3x `float`
- vec<4>
  - 4x `float`
- Name32
  - `uint32_t` - name hash
  - 4 byte - unknown, always 0(?), may be padding or reserved
  - `bool` (i.e. 4 byte) - unknown
- string
  - `uint32_t` len_and_flag = len | 0x80000000 - len always padded to a multiple of 4 bytes (regardless of position in stream)
  - \<raw text data of given len\> - padding with 00 bytes
- uint64_t (8 bytes, be)
- uint32_t (4 bytes, be)
- uint16_t (2 bytes, be)
- uint8_t (1 byte)
- int8_t (1 byte)
- binary (no length field; length padded to multiple of 4 bytes, regardless of position in stream)

## Checksum, Name32 hash algorithm
```python
def compute_checksum(data):
    # Matches 'sdbm' (http://www.cse.yorku.ca/~oz/hash.html#sdbm)
    sum = 0
    for i in range(len(data)):
        sum = ((sum*0x1003F)&0xFFFFFFFF) + data[i]
        sum = sum&0xFFFFFFFF
    return sum
```

## Name32 lookup
The game has an internal lookup to convert from strings to Name32 hashes. Can be dumped from game memory, but appears to be incomplete. 

Memory search for: `44 45 46 41 55 4C 54 00 55 4E 44 45 46 49 4E 45 44 00 4C 65 66 74 00 43 65 6E 74 65 72 00 52 69 67 68 74 00 4A 75 73 74 69 66 79 00 4E 6F 6E 65 00`
Contains a string table (> 3 MiB), each string separated by a '\0' character.
