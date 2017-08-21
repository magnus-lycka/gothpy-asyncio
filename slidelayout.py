import jinja2
import os


class OutOfCellsError(ValueError):
    pass


class Format:
    def __init__(self, cols, rows, skip=None, use=None):
        self.current = 0
        self.y = 0
        self.x = -1
        self.cols = cols
        self.rows = rows
        if skip and use:
            raise ValueError("Don't use both skip and use")
        if use:
            skip = self.use_to_skip(use)
        self.skip = skip or []
        self.skipped = 0

    def use_to_skip(self, use):
        skip = []
        for x in range(self.cols):
            for y in range(self.rows):
                if not (x, y) in use:
                    skip.append((x, y))
        return skip

    @property
    def scale(self):
        return 1 / max(self.cols, self.rows)

    @property
    def rpos(self):
        return (self.x + 0.5) / self.cols , (self.y + 0.5) / self.rows

    def next_cell(self):
        self.x += 1
        if self.x >= self.cols:
            self.x = 0
            self.y += 1
        if self.y >= self.rows:
            raise OutOfCellsError('Out of cells at slide %i!' % self.current)

    def next(self):
        self.next_cell()
        self.skipped = 0
        while (self.x, self.y) in self.skip:
            self.next_cell()
            self.skipped += 1
        self.current += 1


class Layouter:
    def __init__(self):
        self._slide = 0
        self._params = {}
        self._format = []
        self.height = 1000
        self.width = 1600
        self._where_were_we = []
        self._last_x = 0
        self._last_y = 0

    def children(self, cols, rows, skip=None, use=None):
        self._format.append(Format(cols, rows, skip, use))
        self._where_were_we.append((self._last_x, self._last_y))
        return ''

    def _base_coordinates(self):
        return self._where_were_we[-1]

    def _update(self):
        scale = 1
        fmt = None
        for fmt in self._format:
            scale *= fmt.scale
        self._params['data-scale'] = scale
        if fmt:
            fmt.next()
            rel_x, rel_y = fmt.rpos
            base_x, base_y = self._base_coordinates()
            x = (rel_x - 0.5) * self.width * scale / fmt.scale + base_x
            y = (rel_y - 0.5) * self.height * scale / fmt.scale + base_y
            self._last_x = x
            self._last_y = y

            self._params['data-x'] = '%i' % x
            self._params['data-y'] = '%i' % y

    def set(self, **kwargs):
        while 1:
            try:
                self._update()
                break
            except OutOfCellsError:
                self._format.pop()
                self._where_were_we.pop()

        self._params.update({key.replace('_', '-'):value for (key, value) in kwargs.items()})
        return self.write(self._params)

    @staticmethod
    def write(map):
        results = []
        for key, value in map.items():
            results.append(":%s: %s" % (key, value))
        return "\n".join(results) + "\n"


os.chdir('docs')
layout = Layouter()
template = jinja2.Template(open('./gothpy-asyncio.rst').read())

with open('temp.rst', 'w') as out:
    out.write(template.render(layout=layout))

cmd = '/home/mly/.pyenv/versions/3.6.1/bin/hovercraft temp.rst html'
os.system(cmd)

