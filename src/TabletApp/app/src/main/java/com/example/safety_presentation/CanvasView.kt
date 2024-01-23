package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View

class CanvasView (context: Context, attrs: AttributeSet) : View(context, attrs){
    private val mPath: Path = Path()
    private val mPaint : Paint = Paint()
    var lx = 0f
    var ly = 0f

    init{
        mPaint.style = Paint.Style.STROKE
        mPaint.strokeWidth = 5f
    }

    override fun onDraw(canvas: Canvas){
        super.onDraw(canvas)
        canvas.drawPath(mPath, mPaint)
        invalidate()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        val x = event.x
        val y = event.y

        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                mPath.moveTo(x, y)
                lx = x
                ly = y
            }

            MotionEvent.ACTION_MOVE -> {
                mPath.lineTo(x, y)
                lx = x
                ly = y
                invalidate()

            }
        }
        return true
    }

}