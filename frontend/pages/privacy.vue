<template>
  <div class="min-h-screen bg-interview-bg text-interview-text-primary py-12 px-4 sm:px-6 lg:px-8">
    <div
      class="max-w-4xl mx-auto bg-interview-surface backdrop-blur-sm rounded-2xl shadow-xl border border-interview-surface-border overflow-hidden"
    >
      <!-- Header -->
      <div
        class="bg-interview-surface-border/50 px-8 py-6 border-b border-interview-surface-border flex justify-between items-center"
      >
        <h1 class="text-2xl font-bold flex items-center gap-3">
          <span class="text-interview-primary">AI</span> Interview Privacy Policy
        </h1>
        <NuxtLink
          to="/login"
          class="text-interview-text-secondary hover:text-interview-primary transition-colors text-sm font-medium"
        >
          &larr; กลับสู่หน้าล็อคอิน
        </NuxtLink>
      </div>

      <!-- Content -->
      <div class="p-8 space-y-8 text-interview-text-secondary leading-relaxed">
        <section>
          <h2 class="text-xl font-semibold text-interview-text-primary mb-4">
            1. นโยบายความเป็นส่วนตัว (Privacy Policy)
          </h2>
          <p class="mb-4">
            แพลตฟอร์ม AI Interview ("ระบบ") ให้ความสำคัญกับการคุ้มครองข้อมูลส่วนบุคคลของท่าน
            นโยบายนี้อธิบายวิธีการที่เรารวบรวม ใช้
            และเปิดเผยข้อมูลของท่านในการใช้บริการระบบสัมภาษณ์งานอัตโนมัติ
          </p>
        </section>

        <section>
          <h2 class="text-xl font-semibold text-interview-text-primary mb-4">
            2. ข้อมูลที่เราจัดเก็บ
          </h2>
          <ul class="list-disc pl-5 space-y-2">
            <li>
              <strong>ข้อมูลระบุตัวตน:</strong> ชื่อ-นามสกุล, อีเมล, ประวัติการทำงาน (Resume/CV)
            </li>
            <li>
              <strong>ข้อมูลภาพและเสียง:</strong> วิดีโอบันทึกการสัมภาษณ์, ข้อมูลเสียง (Voice Data)
            </li>
            <li>
              <strong>ข้อมูลทางเทคนิค:</strong> IP Address, ประเภทของอุปกรณ์ที่ใช้, ประวัติการใช้งาน
            </li>
          </ul>
        </section>

        <section>
          <h2 class="text-xl font-semibold text-interview-text-primary mb-4">
            3. วัตถุประสงค์การใช้งานข้อมูล
          </h2>
          <p class="mb-4">เราใช้ข้อมูลของท่านเพื่อ:</p>
          <ul class="list-disc pl-5 space-y-2">
            <li>ประมวลผลและวิเคราะห์ผลการสัมภาษณ์งานด้วยระบบ AI</li>
            <li>จัดส่งรายงานผลการประเมินไปยังฝ่ายทรัพยากรบุคคล (HR) ของบริษัท</li>
            <li>ปรับปรุงประสิทธิภาพของระบบ AI (โดยข้อมูลจะถูกทำให้เป็นนิรนาม)</li>
          </ul>
        </section>

        <section>
          <h2 class="text-xl font-semibold text-interview-text-primary mb-4">
            4. การเก็บรักษาข้อมูล
          </h2>
          <p>
            ข้อมูลวิดีโอและผลการประเมินจะถูกจัดเก็บเป็นระยะเวลา 1 ปี
            หรือตามที่บริษัทผู้รับสมัครงานกำหนด หลังจากนั้นระบบจะทำการลบข้อมูลโดยอัตโนมัติ
            หากท่านต้องการลบข้อมูลก่อนกำหนด กรุณาติดต่อฝ่ายบุคคลของผู้บริษัทที่ท่านสมัคร
          </p>
        </section>

        <section>
          <h2 class="text-xl font-semibold text-interview-text-primary mb-4">
            5. การยินยอม (Consent)
          </h2>
          <p>
            โดยการเข้าใช้งานระบบนี้ ท่านยินยอมให้เราบันทึกภาพและเสียงของท่านตลอดระยะเวลาการสัมภาษณ์
            และยินยอมให้ใช้ AI ในการวิเคราะห์ประมวลผลเบื้องต้น
          </p>
        </section>

        <div
          class="mt-8 pt-8 border-t border-interview-surface-border text-sm text-interview-text-muted"
        >
          <p>แก้ไขล่าสุด: {{ new Date().toLocaleDateString('th-TH') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/* No specific logic needed for this static page */
</script>
