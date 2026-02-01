## FastAPI for Beginners - Day 1

### Download Trainging Document

[Click here to download the training document](https://drive.google.com/drive/folders/1jTwWio91_ckDp-9MuXP0EEYPo-TNVAVP?usp=sharing)

### 📋 Content

### Section 1: พื้นฐาน REST API + FastAPI + CRUD เบื้องต้น

1.1 [Overview](#overview)
1.2 [Tools and Editors Required](#tools-and-editors-required)
1.3 [Installing Tools and Configurations](#installing-tools-and-configurations)
1.4 [ความรู้พื้นฐานเกี่ยวกับ API และ HTTP Protocol](#ความรู้พื้นฐานเกี่ยวกับ-api-และ-http-protocol)
1.5 [API คืออะไร ?](#api-คืออะไร-)
1.6 [HTTP Protocol เบื้องต้น](#http-protocol-เบื้องต้น)
1.7 [RESTful API คืออะไร ?](#restful-api-คืออะไร-)
1.8 [GET, POST, PUT, DELETE Methods](#get-post-put-delete-methods)
1.9 [Status Code](#status-code)
1.10 [แนะนำ FastAPI และจุดเด่นของ Framework นี้](#แนะนำ-fastapi-และจุดเด่นของ-framework-นี้)
1.11 [ติดตั้ง Python + uv](#ติดตั้ง-python-+-uv)
1.12 [สร้าง Virtual Environment ด้วย uv](#สร้าง-virtual-environment-ด้วย-uv)
1.13 [สร้าง FastAPI Project แรก](#สร้าง-fastapi-project-แรก)
1.14 [ทดลองสร้าง API Endpoint แรก /hello](#ทดลองสร้าง-api-endpoint-แรก-hello)
1.15 [Structure ของ FastAPI Project](#structure-ของ-fastapi-project)
1.16 [การรับค่า Path, Query, Request Body](#การรับค่า-path-query-request-body)
1.17 [Workshop: สร้างระบบจัดการสินค้า (In-memory CRUD)](#workshop-สร้างระบบจัดการสินค้า-in-memory-crud)

### 1.1 Overview

ในคอร์สนี้เราจะได้เรียนรู้เกี่ยวกับการพัฒนา RESTful API ด้วย FastAPI Framework ซึ่งเป็น Framework ที่ได้รับความนิยมอย่างมากในปัจจุบัน เนื่องจากมีประสิทธิภาพสูงและใช้งานง่าย เราจะเริ่มต้นจากพื้นฐานของ API และ HTTP Protocol จากนั้นจะเรียนรู้การใช้งาน FastAPI ในการสร้าง API Endpoint และการจัดการ CRUD (Create, Read, Update, Delete) โดยไม่ใช้ Database ก่อนที่จะไปสู่การใช้งาน Database ในบทเรียนถัดไป

### 1.2 Tools and Editors Required

1. Visual Studio Code
2. Python 3.14.x
3. UV 0.9.x
4. PostgreSQL 17.x
5. Postman
6. Git

### Verify Tools and Environment on Windows / Mac OS / Linux

Open terminal or command prompt and run the following commands to verify the installations:

### Visual Studio Code

```bash
code --version
```

### Python

```bash
# Windows
python --version
pip --version

# Mac OS / Linux
python3 --version
pip3 --version
```

### UV

```bash
uv --version
```

### PostgreSQL

```bash
psql --version
```

### Git

```bash
git --version
git config --list
```

---

### 1.3 Installing Tools and Configurations

#### Visual Studio Code

- Download and install Visual Studio Code from [here](https://code.visualstudio.com/).

#### Python

- Download and install Python 3.14.x from [here](https://www.python.org/downloads/).
- Make sure to check the option "Add Python to PATH" during installation on Windows.

#### UV

- Install UV using Standalone installer from [here](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac OS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### PostgreSQL

- Download and install PostgreSQL from [here](https://www.postgresql.org/download/).

#### Postman

- Download and install Postman from [here](https://www.postman.com/downloads/).

#### Git

- Download and install Git from [here](https://git-scm.com/downloads).

---

### 1.4 ความรู้พื้นฐานเกี่ยวกับ API และ HTTP Protocol

ในส่วนนี้เราจะได้เรียนรู้เกี่ยวกับพื้นฐานของ API และ HTTP Protocol ซึ่งเป็นสิ่งสำคัญในการพัฒนาเว็บแอปพลิเคชันและบริการต่าง ๆ ที่เกี่ยวข้องกับการสื่อสารระหว่างเครื่องคอมพิวเตอร์ผ่านเครือข่ายอินเทอร์เน็ต

### 1.5 API คืออะไร ?

API (Application Programming Interface) คือชุดของกฎและโปรโตคอลที่ใช้ในการ สื่อสารระหว่างซอฟต์แวร์ต่าง ๆ API ช่วยให้โปรแกรมเมอร์สามารถเข้าถึงฟังก์ชันและข้อมูลของแอปพลิเคชันหรือบริการอื่น ๆ ได้โดยไม่ต้องรู้รายละเอียดภายในของระบบนั้น ๆ

### 1.6 HTTP Protocol เบื้องต้น

HTTP (Hypertext Transfer Protocol) เป็นโปรโตคอลที่ใช้ในการสื่อสารระหว่างเว็บเบราว์เซอร์และเว็บเซิร์ฟเวอร์ HTTP ทำงานบนพื้นฐานของคำขอ (Request) และการตอบกลับ (Response) โดยมีวิธีการหลัก ๆ ดังนี้

- GET: ใช้เพื่อดึงข้อมูลจากเซิร์ฟเวอร์
- POST: ใช้เพื่อส่งข้อมูลไปยังเซิร์ฟเวอร์
- PUT: ใช้เพื่ออัปเดตข้อมูลบนเซิร์ฟเวอร์
- DELETE: ใช้เพื่อลบข้อมูลจากเซิร์ฟเวอร์

### 1.7 RESTful API คืออะไร ?

RESTful API คือรูปแบบหนึ่งของ API ที่ใช้หลักการของ REST (Representational State Transfer) ซึ่งเป็นสถาปัตยกรรมที่ออกแบบมาเพื่อให้บริการเว็บมีความเรียบง่ายและมีประสิทธิภาพ RESTful API ใช้ HTTP Methods ในการดำเนินการต่าง ๆ กับทรัพยากร (Resources) ที่อยู่บนเซิร์ฟเวอร์

### 1.8 GET, POST, PUT, DELETE Methods

ใช้ https://jsonplaceholder.typicode.com/ เป็นตัวอย่าง

- GET: ใช้เพื่อดึงข้อมูลจากเซิร์ฟเวอร์ ตัวอย่างเช่น การ
  ดึงรายชื่อโพสต์
  ```http
  GET /posts
  ```
- POST: ใช้เพื่อส่งข้อมูลไปยังเซิร์ฟเวอร์ ตัวอย่างเช่น การสร้างโพสต์ใหม่
  ```http
  POST /posts
  {
    "title": "foo",
    "body": "bar",
    "userId": 1
  }
  ```
- PUT: ใช้เพื่ออัปเดตข้อมูลบนเซิร์ฟเวอร์ ตัวอย่างเช่น การอัปเดตโพสต์ที่มีอยู่
  ```http
  PUT /posts/1
  {
    "id": 1,
    "title": "foo",
    "body": "bar",
    "userId": 1
  }
  ```
- DELETE: ใช้เพื่อลบข้อมูลจากเซิร์ฟเวอร์ ตัวอย่างเช่น การลบโพสต์
  ```http
  DELETE /posts/1
  ```

### 1.9 Status Code

สถานะของการตอบกลับจากเซิร์ฟเวอร์จะแสดงผ่านรหัสสถานะ (Status Code) ซึ่งแบ่งออกเป็นกลุ่มต่าง ๆ ดังนี้

- 1xx: Informational
- 2xx: Success (เช่น 200 OK, 201 Created)
- 3xx: Redirection
- 4xx: Client Error (เช่น 400 Bad Request, 404 Not Found)
- 5xx: Server Error (เช่น 500 Internal Server Error)

### 1.10 แนะนำ FastAPI และจุดเด่นของ Framework นี้

FastAPI เป็นเว็บเฟรมเวิร์กสำหรับการพัฒนา API ด้วยภาษา Python ที่มีประสิทธิภาพสูงและใช้งานง่าย จุดเด่นของ FastAPI ได้แก่

- ความเร็ว: FastAPI ถูกออกแบบมาให้มีประสิทธิภาพสูง ทำให้สามารถรองรับการร้องขอจำนวนมากได้อย่างรวดเร็ว
- การตรวจสอบข้อมูลอัตโนมัติ: FastAPI ใช้ Pydantic ในการตรวจสอบและแปลงข้อมูล ทำให้การจัดการข้อมูลเป็นเรื่องง่าย
- เอกสารอัตโนมัติ: FastAPI สร้างเอกสาร API อัตโนมัติด้วย Swagger UI และ ReDoc
- รองรับการทำงานแบบ Asynchronous: FastAPI รองรับการเขียนโค้ดแบบ async/await ทำให้สามารถจัดการกับ I/O-bound operations ได้อย่างมีประสิทธิภาพ
- ง่ายต่อการเรียนรู้: FastAPI มีโครงสร้างที่ชัดเจนและใช้งานง่าย เหมาะสำหรับผู้เริ่มต้นและผู้ที่มีประสบการณ์ในการพัฒนาเว็บแอปพลิเคชัน

### 1.11 ติดตั้ง Python + UV

### เกี่ยวกับ uv

**uv** คือ Python package manager ที่รวดเร็วมากและเขียนด้วย Rust สร้างโดยทีม Astral (ทีมเดียวกับที่สร้าง ruff) uv ออกแบบมาเพื่อแทนที่เครื่องมือต่างๆ เช่น:

- `pip`
- `pip-tools`
- `pipx`
- `poetry`
- `pyenv`
- `virtualenv`
- และอื่นๆ

### จุดเด่นของ uv

1. **เร็วมาก** - เร็วกว่า package manager แบบดั้งเดิมหลายเท่า
2. **รองรับได้ดี** - สามารถใช้ร่วมกับเครื่องมือ Python อื่นๆ ได้
3. **จัดการ dependencies** - ใช้ `pyproject.toml` และ `uv.lock` ในการจัดการ dependencies

ตรวจสอบว่าคุณได้ติดตั้ง Python และ uv เรียบร้อยแล้ว โดยใช้คำสั่งต่อไปนี้ในเทอร์มินัลหรือคอมมานด์พรอมต์

```bash
# ตรวจสอบ Python
python --version
# หรือ
python3 --version

# ตรวจสอบ uv
uv --version
```

ถ้ายังไม่ได้ติดตั้ง Python หรือ uv ให้ทำการติดตั้งตามขั้นตอนในหัวข้อ "Installing Tools and Configurations"

### 1.12 สร้าง Virtual Environment ด้วย uv

การสร้าง Virtual Environment ช่วยให้เราสามารถจัดการแพ็กเกจและไลบแพ็กเกจที่ใช้ในโปรเจกต์ได้อย่างอิสระโดยไม่กระทบกับระบบ Python หลักบนเครื่องของเรา

#### 1.12.1 สร้างโฟลเดอร์สำหรับโปรเจกต์ของคุณ

```bash
mkdir fastapi_beginner
```

#### 1.12.2 เข้าไปในโฟลเดอร์โปรเจกต์

```bash
cd fastapi_beginner
```

#### 1.12.3 สร้างโฟลเดอร์โปรเจกต์

```bash
mkdir my_fastapi
```

#### 1.12.4 ทำการ Initialize uv ในโฟลเดอร์โปรเจกต์

```bash
uv init --python  3.13
```

คำสั่งนี้จะสร้างไฟล์:

- `main.py` (สามารถลบได้)
- `pyproject.toml` (ใช้สำหรับจัดการ dependencies และการตั้งค่าโปรเจกต์)
- `.python-version` (ระบุเวอร์ชันของ Python ที่ใช้ในโปรเจกต์)
- `.gitignore` (ใช้สำหรับระบุไฟล์หรือโฟลเดอร์ที่ไม่ต้องการให้ Git ติดตาม)
- `README.md` (ไฟล์เอกสารสำหรับโปรเจกต์)

รู้จักกับไฟล์สำคัญ:

- `pyproject.toml`: ไฟล์นี้ใช้สำหรับจัดการ dependencies และการตั้งค่าโปรเจกต์

```toml
[project]
name = "my-fastapi"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
```

- `uv.lock`: ไฟล์ล็อกที่บันทึกเวอร์ชันของแพ็กเกจที่ติดตั้งในโปรเจกต์ เพื่อให้แน่ใจว่าโปรเจกต์จะใช้แพ็กเกจเวอร์ชันเดียวกันทุกครั้งที่ติดตั้ง

ทดสอบติดตั้ง Virtual Environment สำเร็จหรือไม่:

```bash
uv run python --version
```

คำสั่งนี้จะสร้าง Virtual Environment และรัน Python ภายในสภาพแวดล้อมนั้น

### 1.13 สร้าง FastAPI Project แรก

โครงสร้างโปรเจ็กต์ (แนะนำ)

```
my_fastapi/
├── src/
│   └── app.py
├── pyproject.toml
└── uv.lock
```

#### 1.13.1 ติดตั้ง FastAPI และ Uvicorn

```bash
uv add fastapi uvicorn

# หรือระบุเวอร์ชัน
uv add fastapi==0.124.4 uvicorn==0.38.0
```

อธิบายแพ็กเกจที่ติดตั้ง:

- `fastapi`: เป็นเว็บเฟรมเวิร์กสำหรับการพัฒนา API ด้วยภาษา Python ที่มีประสิทธิภาพสูงและใช้งานง่าย
- `uvicorn`: เป็น ASGI server ที่ใช้รันแอปพลิเคชัน FastAPI

เมื่อคุณติดตั้งแพ็กเกจเหล่านี้แล้ว ไฟล์ `pyproject.toml` ของคุณจะมีลักษณะดังนี้:

```toml
[project]
name = "my-fastapi"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.124.4",
    "uvicorn>=0.38.0",
]
```

และเมื่อเช็คด้วยคำสั่ง `uv pip tree` จะเห็นรายการแพ็กเกจที่ติดตั้งอยู่

```
fastapi v0.124.4                        # 👑 พระเอกของงาน! Web Framework หลักที่เราใช้สร้าง API
├── annotated-doc v0.0.4                # 📄 ตัวช่วยจัดการ Documentation และ Type Hint (เพื่อให้ Swagger UI อ่านค่าได้ถูกต้อง)
├── pydantic v2.12.5                    # 👮 ตำรวจตรวจคนเข้าเมือง! ตัวตรวจสอบข้อมูล (Validation) และแปลงข้อมูล (Serialization)
│   ├── annotated-types v0.7.0          # 🏷️ ตัวช่วยกำหนดเงื่อนไขข้อมูลเพิ่ม (เช่น int ต้อง > 0) ใช้คู่กับ Annotated
│   ├── pydantic-core v2.41.5           # ⚙️ เครื่องยนต์หลักของ Pydantic (เขียนด้วยภาษา Rust เพื่อความเร็วระดับเทพ)
│   │   └── typing-extensions v4.15.0   # 🔌 ตัวเสริมความสามารถเรื่อง Type Hint ให้ Python รุ่นเก่าใช้ฟีเจอร์ใหม่ๆ ได้
│   ├── typing-extensions v4.15.0       # (ใช้ซ้ำ - เป็น dependency ร่วมกัน)
│   └── typing-inspection v0.4.2        # 🔍 แว่นขยายสำหรับส่องดู Type ของตัวแปรตอนรันโปรแกรม
│       └── typing-extensions v4.15.0   # (ใช้ซ้ำ)
├── starlette v0.50.0                   # 🧱 รากฐานของ FastAPI! ดูแลเรื่องเว็บพื้นฐาน (Routing, Request, Response) ที่ FastAPI ยืมมาใช้
│   └── anyio v4.12.0                   # ⚡ หัวใจของระบบ Async! ช่วยให้ Python ทำงานหลายอย่างพร้อมกันได้ (Asynchronous)
│       └── idna v3.11                  # 🌐 ตัวแปลงชื่อโดเมนภาษาต่างดาว (International Domain Name) ให้เป็นมาตรฐาน
└── typing-extensions v4.15.0           # (ใช้ซ้ำ)

uvicorn v0.38.0                         # 🚀 ตัว Server (ASGI) ที่ทำหน้าที่รันโค้ด FastAPI ของเราให้ทำงานบนเน็ตได้
├── click v8.3.1                        # ⌨️ ตัวช่วยสร้าง Command Line Interface (ทำให้เราพิมพ์คำสั่ง `uvicorn main:app` ได้)
│   └── colorama v0.4.6                 # 🎨 ตัวช่วยทำสีตัวอักษรใน Terminal (เช่น สีเขียวตอนรันผ่าน สีแดงตอน Error)
└── h11 v0.16.0                         # 📡 ล่ามแปลภาษา HTTP/1.1 (ช่วยให้ Python คุยกับ Browser รู้เรื่อง)
```

#### 1.13.2 เพิ่มไฟล์ใน src/app.py

เปิดไฟล์ `src/app.py` และแก้ไขโค้ดเป็นดังนี้:

```python
from fastapi import FastAPI

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI()

# สร้างเส้นทาง (route) สำหรับ root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI with uv!"}
```

#### 1.13.3 รันแอปพลิเคชัน FastAPI

ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชัน FastAPI:

```bash
uv run uvicorn src.app:app --reload
```

คำสั่งนี้จะรันแอปพลิเคชัน FastAPI บนเซิร์ฟเวอร์ Uvicorn โดยใช้โค้ดจากไฟล์ `src/app.py` และเปิดใช้งานโหมด `--reload` เพื่อให้เซิร์ฟเวอร์รีโหลดอัตโนมัติเมื่อมีการเปลี่ยนแปลงโค้ด

#### 1.13.4 ทดสอบแอปพลิเคชัน

เปิดเว็บเบราว์เซอร์และไปที่ URL: `http://127.0.0.1:8000/`
คุณจะเห็นข้อความ:

```json
{ "message": "Hello FastAPI with uv!" }
```

แสดงว่าแอปพลิเคชัน FastAPI ของคุณทำงานได้สำเร็จแล้ว!

#### 1.13.5 เข้าถึงเอกสาร API อัตโนมัติ

FastAPI มีฟีเจอร์สร้างเอกสาร API อัตโนมัติด้วย Swagger UI และ ReDoc

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 1.14 ทดลองสร้าง API Endpoint แรก /hello

เพิ่มโค้ดในไฟล์ `src/app.py` ดังนี้:

```python
@app.get("/hello")
def read_hello():
    return {"message": "Hello, this is the /hello endpoint!"}
```

### 1.15 Structure ของ FastAPI Project

โครงสร้างโปรเจ็กต์ FastAPI ที่แนะนำมีดังนี้:

```my_fastapi/
├── src/
│   └── app.py
├── pyproject.toml
└── uv.lock
```

- `src/`: โฟลเดอร์สำหรับเก็บโค้ดแอปพลิเคชัน
- `app.py`: ไฟล์หลักที่ใช้ในการกำหนดเส้นทาง (routes) และฟังก์ชันต่าง ๆ ของแอปพลิเคชัน
- `pyproject.toml`: ไฟล์สำหรับจัดการ dependencies และการตั้งค่าโปรเจกต์
- `uv.lock`: ไฟล์ล็อกที่บันทึกเวอร์ชันของแพ็กเกจที่ติดตั้งในโปรเจกต์

### 1.16 การรับค่า Path, Query, Request Body

ใน FastAPI เราสามารถรับค่าจาก Path, Query, และ Request Body ได้ ดังนี้:

#### 1.16.1 รับค่าจาก Path ใช้เมื่อต้องการระบุ ID หรือ Resource เฉพาะเจาะจง

```python
@app.get("/users/{user_id}")
def get_user(user_id: int): # FastAPI จะแปลงเป็น int ให้เอง
    return {"user_id": user_id}
```

#### 1.16.2 รับค่าจาก Query Parameter (ค้นหา/กรอง)

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

#### 1.16.3 รับค่าจาก Request Body

```python
from pydantic import BaseModel

# สร้าง Schema (พิมพ์เขียว) ของข้อมูลที่คาดว่าจะได้รับใน Request Body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# สร้างเส้นทาง (route) สำหรับสร้างไอเท็มใหม่จากข้อมูลใน request body
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "price_with_tax": item.price * 1.07}

```

#### 1.16.3 ทดลองทดสอบ API Endpoint ต่าง ๆ

- ทดสอบ GET /users/{user_id}
- ทดสอบ GET /items/?skip=5&limit=15
- ทดสอบ POST /items/ โดยส่ง JSON body ดังนี้:

```json
{
  "name": "Sample Item",
  "description": "This is a sample item",
  "price": 100.0,
  "tax": 7.0
}
```

### 1.17 CRUD แบบไม่ใช้ Database (list, dict)

ในส่วนนี้เราจะสร้างระบบ CRUD (Create, Read, Update, Delete) แบบง่าย ๆ โดยไม่ใช้ฐานข้อมูลจริง แต่จะใช้โครงสร้างข้อมูลแบบ list และ dict ในการจัดเก็บข้อมูลชั่วคราว

#### 1.17.1 สร้างไฟล์ src/crud.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 1. จำลอง Database (In-memory)
fake_db = [
    {"id": 1, "name": "Laptop", "price": 25000, "stock": 5},
    {"id": 2, "name": "Mouse", "price": 500, "stock": 20}
]

# 2. สร้าง Schema สำหรับรับ/ส่งข้อมูล
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class ProductUpdate(BaseModel): # สำหรับการอัปเดต (เลือกส่งบางค่าได้)
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# --- API Endpoints ---

# [R]ead All: ดูสินค้าทั้งหมด
@app.get("/products", response_model=List[Product])
def get_products():
    return fake_db

# [R]ead One: ดูสินค้าตาม ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    # วนลูปหา ID ที่ตรงกัน
    for product in fake_db:
        if product["id"] == product_id:
            return product
    # ถ้าหาไม่เจอ ให้โยน Error 404
    raise HTTPException(status_code=404, detail="Product not found")

# [C]reate: เพิ่มสินค้าใหม่
@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    # เช็คว่า ID ซ้ำไหม
    for p in fake_db:
        if p["id"] == product.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    fake_db.append(product.model_dump()) # แปลง Pydantic เป็น Dict แล้วเก็บ
    return product

# [U]pdate: แก้ไขสินค้า
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, update_data: ProductUpdate):
    for index, product in enumerate(fake_db):
        if product["id"] == product_id:
            # Copy ข้อมูลเดิมมา แล้วทับด้วยข้อมูลใหม่เฉพาะที่ส่งมา
            stored_item_model = Product(**product)
            update_data_dict = update_data.model_dump(exclude_unset=True)
            updated_item = stored_item_model.model_copy(update=update_data_dict)

            # บันทึกลง DB
            fake_db[index] = updated_item.model_dump()
            return updated_item

    raise HTTPException(status_code=404, detail="Product not found")

# [D]elete: ลบสินค้า
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(fake_db):
        if product["id"] == product_id:
            fake_db.pop(index)
            return {"message": "Product deleted successfully"}

    raise HTTPException(status_code=404, detail="Product not found")
```

#### 1.17.2 รันแอปพลิเคชัน CRUD

ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชัน CRUD

```bash
uv run uvicorn src.crud:app --reload
```

#### 1.17.3 ทดสอบ API CRUD

- ทดสอบ GET /products
- ทดสอบ GET /products/{product_id}
- ทดสอบ POST /products โดยส่ง JSON body ดังนี้:

```json
{
  "id": 3,
  "name": "Keyboard",
  "price": 1500,
  "stock": 10
}
```

- ทดสอบ PUT /products/{product_id} โดยส่ง JSON body ดังนี้:

```json
{
  "price": 2000,
  "stock": 15
}
```

- ทดสอบ DELETE /products/{product_id}
