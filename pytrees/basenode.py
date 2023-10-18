from typing import Self, Any
from math import floor, ceil, trunc

type S[T] = dict[str, Self | T | list[S[T]]]

class BaseNode[T]:
    def __init__(self, identity: T = None) -> None:
        self._identity = identity

    @property
    def identity(self) -> T:
        return self._identity

    @identity.setter
    def identity(self, identity: T) -> None:
        self._identity = identity

    def is_empty(self) -> bool:
        return self.identity is None
    
    def has_identity(self) -> bool:
        return not self.is_empty()
    
    def is_anonymous(self) -> bool:
        return not self.has_identity()
    
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        return self.identity
    
    def __lt__(self, other: Self) -> bool:
        try:
            return self.identity < other.identity
        except TypeError:
            raise TypeError(f"The '>' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    def __le__(self, other: Self) -> bool:
        try:
            return self.identity <= other.identity
        except TypeError:
            raise TypeError(f"The '>=' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __eq__(self, other: Self) -> bool:
        try:
            return self.identity == other.identity
        except TypeError:
            raise TypeError(f"The '==' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __ne__(self, other: Self) -> bool:
        try:
            return self.identity != other.identity
        except TypeError:
            raise TypeError(f"The '!=' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __gt__(self, other: Self) -> bool:
        try:
            return self.identity > other.identity
        except TypeError:
            raise TypeError(f"The '>' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __ge__(self, other: Self) -> bool:
        try:
            return self.identity >= other.identity
        except TypeError:
            raise TypeError(f"The '>=' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __add__(self, other: Self) -> Self:
        try:
            return self.identity + other.identity
        except TypeError:
            raise TypeError(f"The '+' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __sub__(self, other: Self) -> Self:
        try:
            return self.identity - other.identity
        except TypeError:
            raise TypeError(f"The '-' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __mul__(self, other: Self) -> Self:
        try:
            return self.identity * other.identity
        except TypeError:
            raise TypeError(f"The '*' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __truediv__(self, other: Self) -> Self:
        try:
            return self.identity / other.identity
        except TypeError:
            raise TypeError(f"The '/' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __floordiv__(self, other: Self) -> Self:
        try:
            return self.identity // other.identity
        except TypeError:
            raise TypeError(f"The '//' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __mod__(self, other: Self) -> Self:
        try:
            return self.identity % other.identity
        except TypeError:
            raise TypeError(f"The '%' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __pow__(self, other: Self) -> Self:
        try:
            return self.identity ** other.identity
        except TypeError:
            raise TypeError(f"The '**' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __lshift__(self, other: Self) -> Self:
        try:
            return self.identity << other.identity
        except TypeError:
            raise TypeError(f"The '<<' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rshift__(self, other: Self) -> Self:
        try:
            return self.identity >> other.identity
        except TypeError:
            raise TypeError(f"The '>>' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __and__(self, other: Self) -> Self:
        try:
            return self.identity & other.identity
        except TypeError:
            raise TypeError(f"The '&' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __xor__(self, other: Self) -> Self:
        try:
            return self.identity ^ other.identity
        except TypeError:
            raise TypeError(f"The '^' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __or__(self, other: Self) -> Self:
        try:
            return self.identity | other.identity
        except TypeError:
            raise TypeError(f"The '|' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __radd__(self, other: Self) -> Self:
        try:
            return other.identity + self.identity
        except TypeError:
            raise TypeError(f"The '+' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rsub__(self, other: Self) -> Self:
        try:
            return other.identity - self.identity
        except TypeError:
            raise TypeError(f"The '-' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rmul__(self, other: Self) -> Self:
        try:
            return other.identity * self.identity
        except TypeError:
            raise TypeError(f"The '*' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rtruediv__(self, other: Self) -> Self:
        try:
            return other.identity / self.identity
        except TypeError:
            raise TypeError(f"The '/' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rfloordiv__(self, other: Self) -> Self:
        try:
            return other.identity // self.identity
        except TypeError:
            raise TypeError(f"The '//' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rmod__(self, other: Self) -> Self:
        try:
            return other.identity % self.identity
        except TypeError:
            raise TypeError(f"The '%' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rpow__(self, other: Self) -> Self:
        try:
            return other.identity ** self.identity
        except TypeError:
            raise TypeError(f"The '**' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rlshift__(self, other: Self) -> Self:
        try:
            return other.identity << self.identity
        except TypeError:
            raise TypeError(f"The '<<' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rrshift__(self, other: Self) -> Self:
        try:
            return other.identity >> self.identity
        except TypeError:
            raise TypeError(f"The '>>' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rand__(self, other: Self) -> Self:
        try:
            return other.identity & self.identity
        except TypeError:
            raise TypeError(f"The '&' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __rxor__(self, other: Self) -> Self:
        try:
            return other.identity ^ self.identity
        except TypeError:
            raise TypeError(f"The '^' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ror__(self, other: Self) -> Self:
        try:
            return other.identity | self.identity
        except TypeError:
            raise TypeError(f"The '|' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __iadd__(self, other: Self) -> Self:
        try:
            return self.identity + other.identity
        except TypeError:
            raise TypeError(f"The '+' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __isub__(self, other: Self) -> Self:
        try:
            return self.identity - other.identity
        except TypeError:
            raise TypeError(f"The '-' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __imul__(self, other: Self) -> Self:
        try:
            return self.identity * other.identity
        except TypeError:
            raise TypeError(f"The '*' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __itruediv__(self, other: Self) -> Self:
        try:
            return self.identity / other.identity
        except TypeError:
            raise TypeError(f"The '/' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ifloordiv__(self, other: Self) -> Self:
        try:
            return self.identity // other.identity
        except TypeError:
            raise TypeError(f"The '//' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __imod__(self, other: Self) -> Self:
        try:
            return self.identity % other.identity
        except TypeError:
            raise TypeError(f"The '%' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ipow__(self, other: Self) -> Self:
        try:
            return self.identity ** other.identity
        except TypeError:
            raise TypeError(f"The '**' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ilshift__(self, other: Self) -> Self:
        try:
            return self.identity << other.identity
        except TypeError:
            raise TypeError(f"The '<<' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __irshift__(self, other: Self) -> Self:
        try:
            return self.identity >> other.identity
        except TypeError:
            raise TypeError(f"The '>>' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __iand__(self, other: Self) -> Self:
        try:
            return self.identity & other.identity
        except TypeError:
            raise TypeError(f"The '&' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ixor__(self, other: Self) -> Self:
        try:
            return self.identity ^ other.identity
        except TypeError:
            raise TypeError(f"The '^' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ior__(self, other: Self) -> Self:
        try:
            return self.identity | other.identity
        except TypeError:
            raise TypeError(f"The '|' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __neg__(self) -> Self:
        try:
            return -self.identity
        except TypeError:
            raise TypeError(f"The '-' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __pos__(self) -> Self:
        try:
            return +self.identity
        except TypeError:
            raise TypeError(f"The '+' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __abs__(self) -> Self:
        try:
            return abs(self.identity)
        except TypeError:
            raise TypeError(f"The 'abs()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __invert__(self) -> Self:
        try:
            return ~self.identity
        except TypeError:
            raise TypeError(f"The '~' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __round__(self, n: int = 0) -> Self:
        try:
            return round(self.identity, n)
        except TypeError:
            raise TypeError(f"The 'round()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __floor__(self) -> Self:
        try:
            return floor(self.identity)
        except TypeError:
            raise TypeError(f"The 'floor()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __ceil__(self) -> Self:
        try:
            return ceil(self.identity)
        except TypeError:
            raise TypeError(f"The 'ceil()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __trunc__(self) -> Self:
        try:
            return trunc(self.identity)
        except TypeError:
            raise TypeError(f"The 'trunc()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __float__(self) -> Self:
        try:
            return float(self.identity)
        except TypeError:
            raise TypeError(f"The 'float()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __int__(self) -> Self:
        try:
            return int(self.identity)
        except TypeError:
            raise TypeError(f"The 'int()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __complex__(self) -> Self:
        try:
            return complex(self.identity)
        except TypeError:
            raise TypeError(f"The 'complex()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __bool__(self) -> Self:
        try:
            return bool(self.identity)
        except TypeError:
            raise TypeError(f"The 'bool()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __str__(self) -> str:
        try:
            return str(self.identity)
        except TypeError:
            raise TypeError(f"The 'str()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __repr__(self) -> str:
        try:
            return repr(self.identity)
        except TypeError:
            raise TypeError(f"The 'repr()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __len__(self) -> int:
        try:
            return len(self.identity)
        except TypeError:
            raise TypeError(f"The 'len()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __contains__(self, item: Any) -> bool:
        try:
            return item in self.identity
        except TypeError:
            raise TypeError(f"The 'in' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __getitem__(self, key: Any) -> Any:
        try:
            return self.identity[key]
        except TypeError:
            raise TypeError(f"The '[]' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            self.identity[key] = value
        except TypeError:
            raise TypeError(f"The '[]' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __delitem__(self, key: Any) -> None:
        try:
            del self.identity[key]
        except TypeError:
            raise TypeError(f"The '[]' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
    
    def __iter__(self) -> Any:
        try:
            return iter(self.identity)
        except TypeError:
            raise TypeError(f"The 'iter()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __reversed__(self) -> Any:
        try:
            return reversed(self.identity)
        except TypeError:
            raise TypeError(f"The 'reversed()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __missing__(self, key: Any) -> Any:
        try:
            return self.identity[key]
        except TypeError:
            raise TypeError(f"The '[]' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __hash__(self) -> int:
        try:
            return hash(self.identity)
        except TypeError:
            raise TypeError(f"The 'hash()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __dir__(self) -> list[str]:
        try:
            return dir(self.identity)
        except TypeError:
            raise TypeError(f"The 'dir()' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __getattr__(self, name: str) -> Any:
        try:
            return getattr(self.identity, name)
        except TypeError:
            raise TypeError(f"The '.' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __setattr__(self, name: str, value: Any) -> None:
        try:
            setattr(self.identity, name, value)
        except TypeError:
            raise TypeError(f"The '.' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __delattr__(self, name: str) -> None:
        try:
            delattr(self.identity, name)
        except TypeError:
            raise TypeError(f"The '.' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __enter__(self) -> Self:
        try:
            return self.identity.__enter__()
        except TypeError:
            raise TypeError(f"The 'with' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        try:
            self.identity.__exit__(exc_type, exc_value, traceback)
        except TypeError:
            raise TypeError(f"The 'with' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __await__(self) -> Any:
        try:
            return self.identity.__await__()
        except TypeError:
            raise TypeError(f"The 'await' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __aiter__(self) -> Any:
        try:
            return self.identity.__aiter__()
        except TypeError:
            raise TypeError(f"The 'aiter' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __anext__(self) -> Any:
        try:
            return self.identity.__anext__()
        except TypeError:
            raise TypeError(f"The 'anext' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __aenter__(self) -> Any:
        try:
            return self.identity.__aenter__()
        except TypeError:
            raise TypeError(f"The 'aenter' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        try:
            self.identity.__aexit__(exc_type, exc_value, traceback)
        except TypeError:
            raise TypeError(f"The 'aexit' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __index__(self) -> int:
        try:
            return self.identity.__index__()
        except TypeError:
            raise TypeError(f"The 'index' operation is not supported for identity objects of type '{type(self.identity).__name__}'.")
        
    def __del__(self) -> None:
        try:
            self.identity.__del__()
        except TypeError:
            raise TypeError(f"The 'del' operation is not supported for identity objects of type '{type(self.identity).__name__}'.") 