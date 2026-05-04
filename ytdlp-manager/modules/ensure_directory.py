from pathlib import Path


def ensure_directory(path_input: str) -> Path:
        path = Path(path_input).expanduser()

        try:
            if path.exists():
                if not path.is_dir():
                    raise ValueError(f"Path exists but is not a directory: {path}")
            else:
                path.mkdir(parents= True, exist_ok=False)

            return path
        except PermissionError:
            raise PermissionError(f"No permission to create/access: {path}")
        except OSError as e:
            raise OSError(f"Invalid or restricted path: {path}\n{e}")