import magenta
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.music import constants
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

# Load the model.
bundle_file = magenta.music.notebook_utils.download_bundle('basic_rnn.mag', 'models/')
bundle = magenta.music.sequence_generator_bundle.read_bundle_file(bundle_file)
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# Define the generation parameters.
qpm = constants.DEFAULT_QUARTERS_PER_MINUTE  # tempo
seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
total_seconds = 120  # total time for the generated piece

# Construct the generator options.
generator_options = generator_pb2.GeneratorOptions()
generator_options.args['temperature'].float_value = 1.0  # Higher temperature values increase randomness.
generate_section = generator_options.generate_sections.add(start_time=0, end_time=total_seconds)
generator_options.generate_sections.extend([generate_section])

# Generate the sequence.
sequence = melody_rnn.generate(music_pb2.NoteSequence(), generator_options)

# Save the sequence to a MIDI file.
magenta.music.midi_io.note_sequence_to_midi_file(sequence, 'generated.mid')

# Now, for infinite loop, we need an external midi player which can loop a midi file indefinitely.
