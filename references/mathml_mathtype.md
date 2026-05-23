# MathType-Compatible Equations

## Default Rule

For HTML/PDF outputs, use MathML as the MathType-compatible equation source.

Do:

- Embed MathML directly in `paper_zh_layout.html`.
- Save the same MathML as `assets/equations/<equation-id>.mml`.
- Include a TeX annotation when practical:

```xml
<annotation encoding="application/x-tex">C_x=\frac{N}{N_1}\frac{1}{R_{ref}f_{ref}}</annotation>
```

Do not:

- Claim that HTML or PDF contains editable MathType OLE objects.
- Replace equations with screenshots unless reconstruction is too uncertain.

## Minimal MathML Pattern

```xml
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <semantics>
    <mrow>...</mrow>
    <annotation encoding="application/x-tex">...</annotation>
  </semantics>
</math>
```

## When Extraction Is Weak

If PDF text extraction corrupts a formula:

1. Inspect the rendered page image.
2. Rebuild the equation from visual evidence and nearby prose.
3. Mark the equation confidence in `source_map.json`.
4. Note the reconstruction in `translation_notes.md`.
