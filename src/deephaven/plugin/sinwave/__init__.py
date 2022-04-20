from __future__ import annotations

from deephaven.plugin import Registration
from deephaven.plugin.object \
    import Exporter, ObjectType, Reference

__version__ = "0.0.1.dev1"

# Class defines a Sin example object
# You can set the count of series, and the size each series will be
class SinWave:
    def __init__(self, count = 1, size = 100) -> None:
        self._count = count
        self._size = size

    @property
    def count(self):
        return self._count

    @property
    def size(self):
        return self._size

class SinWaveType(ObjectType):
    @property
    def name(self) -> str:
        return "deephaven.plugin.sin-wave.SinWave"

    def is_type(self, object) -> bool:
        return isinstance(object, SinWave)

    def to_bytes(self, exporter: Exporter, sin_wave: SinWave) -> bytes:
        from deephaven import empty_table
        from deephaven import _wrapper
        from deephaven.plot.figure import Figure
        from deephaven.table_listener import _do_locked
        import jpy

        # We need to get the liveness scope so we can run table operations
        LivenessScope = jpy.get_type('io.deephaven.engine.liveness.LivenessScope')
        LivenessScopeStack = jpy.get_type('io.deephaven.engine.liveness.LivenessScopeStack')
        liveness_scope = LivenessScope(True)
        LivenessScopeStack.push(liveness_scope)

        series_count = sin_wave.count

        def create_tables():
            # Create the table for inputs
            inputs = jpy.get_type('io.deephaven.engine.table.impl.util.KeyedArrayBackedMutableTable').make(empty_table(series_count).update_view(['Series="" + i', "A=1.0d", "f=1.0d", "b=0.0d"]).j_table, 'Series')
            exporter.reference(inputs)

            result = Figure()
            for s in range(0, series_count):
                t = empty_table(100).join(_wrapper.wrap_j_object(inputs.where("Series = `" + str(s) + "`")), "").update_view(["x=i", "y=A*Math.sin(x*f) + b"])
                exporter.reference(t)
                result = result.plot_xy(series_name="Series" + str(s), t=t, x="x", y="y").show()

            exporter.reference(result)

        _do_locked(create_tables)

        exporter.reference(liveness_scope)
        LivenessScopeStack.pop(liveness_scope)
        return str.encode("{ \"count\": " + str(sin_wave.count) + ", \"size\": " + str(sin_wave.size) + "}")


class SinWaveRegistration(Registration):
    @classmethod
    def register_into(cls, callback: Registration.Callback) -> None:
        callback.register(SinWaveType)
