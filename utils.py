from typing import List, Literal, LiteralString, Dict





FetchRes = Dict[
    Literal["data"], List[
        Dict[
            Literal["id"] | Literal["name"], int | str
        ]
    ]
]





