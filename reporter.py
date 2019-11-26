class Reporter:
  @staticmethod
  def write_output(
    file_name = "output.txt",
    content = "",
    should_overwrite_file = False
  ):
    option = "w+" if should_overwrite_file else "a"
    f = open(file_name, option)

    f.write(
      ""
      + content
    )

    f.close()
