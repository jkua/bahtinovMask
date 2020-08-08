#!/usr/bin/env python3

import os
import math

import svgwrite


class BahtinovMask(object):

    def __init__(self, outputPath, size=100, spacing=1, angle=20, cornerRadius=5):
        self.outputPath = outputPath
        self.size = size
        self.spacing = spacing
        self.angle = angle
        self.cornerRadius = cornerRadius
        self.angleRad = angle/180*math.pi
        self.gapHorizonalSpacing = self.spacing / math.tan(self.angleRad)

        self.dwg = svgwrite.Drawing(outputPath, profile='tiny', size=(f'{size}mm', f'{size}mm'), viewBox=(f'0 0 {size} {size}'))

    def generate(self):

        path = svgwrite.path.Path(stroke=svgwrite.rgb(0, 0, 255), fill='none', stroke_width=0.2)

        # Main lines
        numLines = int(self.size / self.spacing / 2)
        
        for i in range(numLines):
            # Plot descenders
            startX = 0
            startY = self.size/2 + i * self.spacing

            midXOffset = self.size/2
            midYOffset = 0

            endXOffset = self.size/2
            endYOffset = endXOffset * math.tan(self.angleRad)
            if (endYOffset + startY) > self.size:
                endYOffset = self.size - startY
                endXOffset = endYOffset/math.tan(self.angleRad)

            path.push(f'M{startX:.6f},{startY:.6f} l{midXOffset:.6f},{midYOffset:.6f} l{endXOffset:.6f},{endYOffset:.6f}')

            # Plot ascenders
            startY = self.size/2 - i * self.spacing
            if i == 0:
                path.push(f'M{startX:.6f},{startY:.6f} m{midXOffset:.6f},{midYOffset:.6f} l{endXOffset:.6f},{-endYOffset:.6f}')
            else:
                path.push(f'M{startX:.6f},{startY:.6f} l{midXOffset:.6f},{midYOffset:.6f} l{endXOffset:.6f},{-endYOffset:.6f}')

        # Gap lines
        numLines = int(self.size / self.gapHorizonalSpacing / 2) + 1
        for i in range(1, numLines):
            midX = self.size/2 + i * self.gapHorizonalSpacing
            midY = self.size/2

            startX = self.size
            startY = (startX - midX) * math.tan(self.angleRad) + midY
            if (startY) > self.size:
                startY = self.size
                startX = self.size - (startY - midY)/math.tan(self.angleRad)

            endX = startX
            if endX == self.size:
                endY = midY - (startX - midX) * math.tan(self.angleRad)
            else:
                endY = 0

            path.push(f'M{startX:.6f},{startY:.6f} L{midX:.6f},{midY:.6f} L{endX:.6f},{endY:.6f}')

        self.dwg.add(path)

        # Frame
        self.dwg.add(self.dwg.rect((0,0), (self.size, self.size), rx=self.cornerRadius, ry=self.cornerRadius, stroke=svgwrite.rgb(255, 0, 0), fill='none', stroke_width=0.2))
        self.dwg.save()


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='.', help='Output path')
    parser.add_argument('--size', type=float, default=100, help='Size in mm')
    parser.add_argument('--spacing', type=float, default=1, help='Line spacing in mm')
    parser.add_argument('--angle', type=float, default=20, help='Pattern angle in degrees')
    parser.add_argument('--cornerRadius', type=float, default=5, help='Corner radius in mm')
    args = parser.parse_args()

    if args.size <= 0:
        raise Exception('Size must be positive and non-zero!')
    if args.spacing <= 0:
        raise Exception('Spacing must be postive and non-zero!')
    if args.angle < 0 or args.angle >= 90:
        raise Exception('Mask angle must be between 0 and 90!')
    if args.cornerRadius < 0 or args.cornerRadius > args.size/2:
        raise Exception('Corner radius must be between 0 and size/2!')

    outputPath = os.path.join(args.output, f'bahtinovMask_{args.size:.1f}mm_spacing{args.spacing:.1f}mm_angle{args.angle:.1f}deg.svg')
    mask = BahtinovMask(outputPath, args.size, args.spacing, args.angle, args.cornerRadius)
    mask.generate()